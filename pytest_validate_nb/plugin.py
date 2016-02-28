"""
pytest ipython plugin modification

Authors: D. Cortes, O. Laslett, T. Kluyver

"""

# import the pytest API
import pytest
import os
import sys
import re
from collections import OrderedDict

# for python 3 compatibility
PY3 = sys.version_info[0] >= 3
import six

# Kernel for jupyter notebooks
from jupyter_client.manager import start_new_kernel

try:
    from Queue import Empty
except:
    from queue import Empty

# for reading notebook files
from nbformat import reads, NotebookNode

# define colours for pretty outputs
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class NbCellError(Exception):
    """ custom exception for error reporting. """


def pytest_addoption(parser):
    """
    Adds the --ipynb option flag for py.test.

    Adds an optional flag to pass a config file with regex
    expressions to sanitise the outputs
    Only will work if the --ipynb flag is present

    This is called by the pytest API
    """
    group = parser.getgroup("general")
    group.addoption('--ipynb', action='store_true',
                    help="Validate IPython notebooks")

    group.addoption('--sanitize-with',
                    help='File with regex expressions to sanitize '
                         'the outputs. This option only works when '
                         'the --ipynb flag is passed to py.test')


def pytest_collect_file(path, parent):
    """
    Collect IPython notebooks using the specified pytest hook
    """
    if path.fnmatch("*.ipynb") and parent.config.option.ipynb:
        return IPyNbFile(path, parent)



class RunningKernel(object):
    """
    Running a Kernel a Jupyter, info can be found at:
    http://jupyter-client.readthedocs.org/en/latest/messaging.html

    The purpose of this class is to encapsulate interaction with the
    jupyter kernel. Thus any changes on the jupyter side to how
    kernels are started/managed should not require any changes outside
    this class.

    """
    def __init__(self):
        """
        Initialise a new kernel
        specfiy that matplotlib is inline and connect the stderr.
        Stores the active kernel process and its manager.
        """
        self.km, self.kc = \
                start_new_kernel(extra_arguments=['--matplotlib=inline'],
                                  stderr=open(os.devnull, 'w'))


    def get_message(self, timeout=None):
        """
        Function is used to get a message from the iopub channel.
        Timeout is None by default
        When timeout is reached
        """
        return self.kc.get_iopub_msg(timeout=timeout)

    def execute_cell_input(self, cell_input, allow_stdin=None):
        """
        Executes a string of python code in cell input.
        We do not allow the kernel to make requests to the stdin
             this is the norm for notebooks

        Function returns a unique message id of the reply from
        the kernel.
        """
        return self.kc.execute(cell_input, allow_stdin=allow_stdin)


    # These options are in case we wanted to restart the nb every time
    # it is executed a certain task
    def restart(self):
        """
        Instructs the kernel manager to restart the kernel process now.
        """
        self.km.restart_kernel(now=True)


    def stop(self):
        """
        Instructs the kernel process to stop channels
        and the kernel manager to then shutdown the process.
        """
        self.kc.stop_channels()
        self.km.shutdown_kernel(now=True)
        del self.km


class IPyNbFile(pytest.File):
    """
    This class represents a pytest collector object.
    A collector is associated with an ipynb file and collects the cells
    in the notebook for testing.
    yields pytest items that are required by pytest.
    """
    def __init__(self, *args, **kwargs):
        super(IPyNbFile, self).__init__(*args, **kwargs)
        self.sanitize_patterns = OrderedDict()  # Filled in setup_sanitize_patterns()

    def setup(self):
        """
        Called by pytest to setup the collector cells in .
        Here we start a kernel and setup the sanitize patterns.
        """
        self.kernel = RunningKernel()
        self.setup_sanitize_files()


    def setup_sanitize_files(self):
        """
        For each of the sanitize files that were specified as command line options
        load the contents of the file into the sanitise patterns dictionary.
        """
        for fname in self.get_sanitize_files():
            with open(fname, 'r') as f:
                self.sanitize_patterns.update(get_sanitize_patterns(f.read()))


    def get_sanitize_files(self):
        """
        Return list of all sanitize files provided by the user on the command line.

        N.B.: We only support one sanitize file at the moment, but
              this is likely to change in the future

        """
        if self.parent.config.option.sanitize_with is not None:
            return [self.parent.config.option.sanitize_with]
        else:
            return []

    def get_kernel_message(self, timeout=None):
        """
        Gets a message from the iopub channel of the notebook kernel.
        """
        return self.kernel.get_message(timeout=timeout)

    # Read through the specified notebooks and load the data
    # (which is in json format)
    def collect(self):
        """
        The collect function is required by pytest and is used to yield pytest
        Item objects. We specify an Item for each code cell in the notebook.
        """
        with self.fspath.open() as f:
            self.nb = reads(f.read(), 4)

            # Start the cell count
            cell_num = 0

            # Iterate over the cells in the notebook
            for cell in self.nb.cells:
                # Skip the cells that have text, headings or related stuff
                # Only test code cells
                if cell.cell_type == 'code':
                    # If the code is a notebook magic cell, do not execute it
                    if cell.source.startswith('%%'):
                        continue

                    # If a cell starts with the comment string
                    # PYTEST_VALIDATE_IGNORE_OUTPUT then test that the cell
                    # executes without fail but do not compare the outputs.
                    elif (cell.source.startswith(r'# PYTEST_VALIDATE_IGNORE_OUTPUT') or
                            cell.source.startswith(r'#PYTEST_VALIDATE_IGNORE_OUTPUT')):
                        yield IPyNbCell(self.name, self, cell_num,
                                        cell, docompare=False)

                    # otherwise yield a full test (the normal case)
                    else:
                        yield IPyNbCell(self.name, self, cell_num, cell)

                # Update 'code' cell count
                cell_num += 1

    def teardown(self):
        self.kernel.stop()


class IPyNbCell(pytest.Item):
    def __init__(self, name, parent, cell_num, cell, docompare=True):
        super(IPyNbCell, self).__init__(name, parent)

        # Store reference to parent IPynbFile so that we have access
        # to the running kernel.
        self.parent = parent

        self.cell_num = cell_num
        self.cell = cell

        self.comparisons = None
        self.docompare = docompare

    """ *****************************************************
        *****************  TESTING FUNCTIONS  ***************
        ***************************************************** """

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        if isinstance(excinfo.value, NbCellError):
            msg_items = [bcolors.FAIL + "Notebook cell execution failed" + bcolors.ENDC]
            formatstring = bcolors.OKBLUE + "Cell %d: %s\n\n" + \
                    "Input:\n" + bcolors.ENDC + "%s\n\n" + \
                    bcolors.OKBLUE + "Traceback:%s" + bcolors.ENDC
            msg_items.append(formatstring % excinfo.value.args)
            return "\n".join(msg_items)
        else:
            return "pytest plugin exception: %s" % str(excinfo.value)

    def reportinfo(self):
        description = "cell %d" % self.cell_num
        return self.fspath, 0, description

    def compare_outputs(self, test, ref, skip_compare=('metadata',
                                                       'image/png',
                                                       'traceback',
                                                       'latex',
                                                       'prompt_number',
                                                       'stdout',
                                                       'stream',
                                                       'output_type',
                                                       'name',
                                                       'execution_count'
                                                       )):
        self.comparisons = []

        # For every different key, we will store the outputs in a
        # single string, in a dictionary with the same keys
        # At the end, every dictionary entry will be compared
        # We skip the unimportant keys in the 'skip_compare' list
        #
        # We concatenate the outputs because the ipython notebook produces
        # them in a random number of dictionaries. So, it is easier
        # to compare only one chunk of data
        testing_outs, reference_outs = {}, {}

        # Check the references (embedded notebook outputs)
        # and start appendind the outputs for every
        # different key. The entries of every output have the structure:
        #
        # {'output_type': 'stream', 'stream': 'stdout',
        #  'text': "The time is: 11:44:21\nToday's date is: 13/03/15\n"}
        #
        # We discard the keys from the skip_compare list
        for reference in ref:
            for key in reference.keys():
                if key not in skip_compare:

                    # In the EXECUTION, we already processed the display_data
                    # (or execute_count)
                    # kind of dictionary entries. display_data has a 'data'
                    # sub dictionary which contains the relevant information
                    # about the Figure: 'text/plain', 'image/png', ...
                    #
                    # EXAMPLES:
                    #
                    # display_data type:
                    # {'output_type': 'display_data', 'image/png': 'iVBORw0...
                    #  'text/plain': <matplotlib.figure.Figure at 0x7f9ca97cc890>
                    #  'metadata': {} }
                    #
                    #
                    # Hence, we look into these sub dictionary entries and
                    # append them to the corresponding dictionary entry
                    # in the reference outputs
                    #
                    if key == 'data':
                        for data_key in reference[key].keys():
                            # Filter the keys in the SUB-dictionary again
                            if data_key not in skip_compare:
                                try:
                                    reference_outs[data_key] += self.sanitize(reference[key][data_key])
                                except:
                                    reference_outs[data_key] = self.sanitize(reference[key][data_key])


                    # NOTICE: that execute_result (similar for figures than
                    # display_data but without the png or picture hex)
                    # has an 'execution_count' key
                    # which we skip because is not relevant for now.
                    # We could use this in the future if we wanted executions
                    # in the same order than the reference
                    #
                    # execute_result type:
                    # {'output_type': 'execute_result', 'execution_count': 9,
                    #  'text/plain': '<matplotlib.image.AxesImage at 0x7f9ca8f058d0>',
                    #  'metadata': {}}

                    # Otherwise, just create a normal dictionary entry from
                    # one of the keys of the dictionary
                    else:
                        # Create the dictionary entries on the fly, from the
                        # existing ones to be compared
                        try:
                            reference_outs[key] += self.sanitize(reference[key])
                        except:
                            reference_outs[key] = self.sanitize(reference[key])

        # the same for the testing outputs (the cells that are boing executed)
        # display_data cells were already processed! (see the execution loop)
        for testing in test:
            for key in testing.keys():
                # For debugging:
                # print 'TESTING:', key, '---', testing[key]
                if key not in skip_compare:
                    try:
                        testing_outs[key] += self.sanitize(testing[key])
                    except:
                        testing_outs[key] = self.sanitize(testing[key])

        for key in reference_outs.keys():
            # For debugging:
            # print 'REFERENCE:', key, '---', reference_outs[key]

            # Check if they have the same keys
            if key not in testing_outs.keys():
                self.comparisons.append(bcolors.FAIL
                                        + "missing key: TESTING %s != REFERENCE %s"
                                        % (testing_outs.keys(), reference_outs.keys())
                                        + bcolors.ENDC)
                return False

            # Compare the large string from the corresponding dictionary entry
            # We use str() to be sure that the unicode key strings from the
            # reference are also read from the testing dictionary
            if testing_outs[str(key)] != reference_outs[key]:

                # print testing_outs[key]
                # print reference_outs[key]

                self.comparisons.append(bcolors.OKBLUE
                                        + " mismatch '%s'\n" % key
                                        + bcolors.FAIL
                                        + "<<<<<<<<<<<< Reference output from ipynb file:"
                                        + bcolors.ENDC)
                self.comparisons.append(reference_outs[key])
                self.comparisons.append(bcolors.FAIL
                                        + '============ disagrees with newly computed (test) output:  '
                                        + bcolors.ENDC)
                self.comparisons.append(testing_outs[str(key)])
                self.comparisons.append(bcolors.FAIL
                                        + '>>>>>>>>>>>>'
                                        + bcolors.ENDC)

                # self.comparisons.append('==============')
                # self.comparisons.append('The absolute test string:')
                # self.comparisons.append(self.sanitize(test[key]))
                # self.comparisons.append('failed to compare with the reference:')
                # self.comparisons.append(self.sanitize(ref[key]))

                return False
        return True


    """ *****************************************************
        ***************************************************** """

    def runtest(self):
        """
        Run all the cell tests in one kernel without restarting.
        It is very common for ipython notebooks to run through assuming a
        single kernel.
        """
        # Execute the code from the current cell and get the msg_id
        # of the shell process.
        msg_id = self.parent.kernel.execute_cell_input(
            self.cell.source, allow_stdin=False)

        # Time for the reply of the cell execution
        # (maximum time, it can finish before, we could make a timeout
        # exception in the future)
        timeout = 2000

        # This list stores the output information for the entire cell
        outs = []

        # Wait for the execution reply (we can see this in the msg_type)
        # This execution produces a dictionary where a status string can be
        # obtained: 'ok' OR 'error' OR 'abort'
        # We can also get how many cells have been executed
        # until here, with the 'execution_count' entry
        # self.parent.kernel.kc.get_shell_msg(timeout=timeout)

        while True:
            """
            The messages from the cell contain information such
            as input code, outputs generated
            and other messages. We iterate through each message
            until we reach the end of the cell.
            """
            try:
                # Get one message at a time, per code block inside the cell
                msg = self.parent.get_kernel_message(timeout=timeout)

            except Empty:
                # This is not working: ! The code will not be checked
                # if the time is out (when the cell stops to be executed?)
                # raise NbCellError("Timeout of %d seconds exceeded"
                #                      " executing cell: %s" (timeout,
                #                                             self.cell.input))
                # Just break the loop when the output is empty
                break

            """
            Now that we have the output from a piece of code
            inside the cell,
            we want to compare the outputs of the messages
            to a reference output (the ones that are present before
            the notebook was executed)
            """

            # print msg

            # Firstly, get the msg type from the cell to know if
            # the output comes from a code
            # It seems that the type 'stream' is irrelevant
            msg_type = msg['msg_type']
            reply = msg['content']

            # REF:
            # execute_input: To let all frontends know what code is
            # being executed at any given time, these messages contain a
            # re-broadcast of the code portion of an execute_request,
            # along with the execution_count.
            if msg_type == 'status':
                if reply['execution_state'] == 'idle':
                    break
                else:
                    continue
            elif msg_type == 'execute_input':
                continue
            elif msg_type.startswith('comm'):
                continue
            elif msg_type == 'execute_reply':
                # print msg
                continue
            # If there is no more output, continue with the executions
            # (it will break if it is empty, with the previous statements)
            #
            # REF:
            # This message type is used to clear the output that is
            # visible on the frontend
            # elif msg_type == 'clear_output':
            #     outs = []
            #     continue

            # I added the msg_type 'idle' condition (when the cell stops)
            # so we get a complete cell output
            # REF:
            # When the kernel starts to execute code, it will enter the 'busy'
            # state and when it finishes, it will enter the 'idle' state.
            # The kernel will publish state 'starting' exactly
            # once at process startup.
            # elif (msg_type == 'clear_output'
            #       and msg_type['execution_state'] == 'idle'):
            #     outs = []
            #     continue

            """
            Now we get the reply from the piece of code executed
            and analyse the outputs
            """
            reply = msg['content']

            # Debugging
            if msg_type == 'stream' and reply['text'].startswith('PTVNB-DBG:'):
                print(reply['text'])
                continue

            out = NotebookNode(output_type=msg_type)

            # print '---------------------------- CELL ----------------------'
            # print msg_type
            # print reply
            # print '---------------------------- CELL ORIGINAL----------------'
            # print self.cell.outputs

            # Now check what type of output it is
            if msg_type == 'stream':
                out.stream = reply['name']
                out.text = reply['text']

            # REF:
            # 'execute_result' is equivalent to a display_data message.
            # The object being displayed is passed to the display
            # hook, i.e. the *result* of the execution.
            # The only difference is that 'execute_result' has an
            # 'execution_count' number which does not seems useful
            # (we will filter it in the sanitize function)
            #
            # When the reply is display_data or execute_count,
            # the dictionary contains
            # a 'data' sub-dictionary with the 'text' AND the 'image/png'
            # picture (in hexadecimal). There is also a 'metadata' entry
            # but currently is not of much use, sometimes there is information
            # as height and width of the image (CHECK the documentation)
            # Thus we iterate through the keys (mimes) 'data' sub-dictionary
            # to obtain the 'text' and 'image/png' information
            #
            # We NO longer replace 'image/png' by 'png' since the last version
            # of the notebook format is more consistent. We also DO NOT
            # replace any .xml string, it's not neccesary

            # elif msg_type in ('display_data', 'execute_result'):
            elif msg_type in ('display_data', 'execute_result'):
                out['metadata'] = reply['metadata']
                for mime, data in six.iteritems(reply['data']):
                # This could be useful for reference or backward compatibility
                #     attr = mime.split('/')[-1].lower()
                #     attr = attr.replace('+xml', '').replace('plain', 'text')
                #     setattr(out, attr, data)

                # Return the relevant entries from data:
                # plain/text, image/png, execution_count, etc
                # We coul use a mime types list for this (MAYBE)
                    setattr(out, mime, data)

                # if msg_type == 'execute_result':
                #     out.prompt_number = reply['execution_count']

            elif msg_type == 'error':
                traceback = '\n' + '\n'.join(reply['traceback'])
                raise NbCellError(self.cell_num, "Cell execution caused an exception",
                                  self.cell.source, traceback)

            else:
                print("unhandled iopub msg:", msg_type)

            outs.append(out)

        """
        This message is the last message of the cell, which contains no output.
        It only indicates whether the entire cell ran successfully or if there
        was an error.
        """
        # reply = msg['content']

        failed = False

        # THIS COMPARISON IS ONLY WHEN THE OUTPUT DICTIONARIES
        # ARE DIFFERENT, WHICH IS A DIFFERENT ERROR, not
        # from the output in the notebook
        #
        # SINCE WE SANITIZE AND COMPARE, IF THERE ARE DIFFERENT
        # NUMBER OF LINES, this error will be reported
        #
        # Compare if the outputs have the same number of lines
        # and throw an error if it fails
        # if len(outs) != len(self.cell.outputs):
        #     self.diff_number_outputs(outs, self.cell.outputs)
        #     failed = True

        # If the outputs are the same, compare them line by line
        # else:
        # for out, ref in zip(outs, self.cell.outputs):
        if self.docompare:
            if not self.compare_outputs(outs, self.cell.outputs):
                failed = True

        # if reply['status'] == 'error':
        # Traceback is only when an error is raised (?)

        # We usually get an exception because traceback is not defined
        if failed:  # Use this to make the test fail
            """
            The pytest exception will be raised if there are any
            errors in the notebook cells. Now we check that
            the outputs produced from running each cell
            matches the outputs in the existing notebook.
            This code is taken from [REF].
            """
            raise NbCellError(self.cell_num,
                              # Still needs correction. We could
                              # add a description
                              "Error with cell",
                              self.cell.source,
                              # Here we must put the traceback output:
                              '\n'.join(self.comparisons))

    def sanitize(self, s):
        """sanitize a string for comparison.

        fix universal newlines, strip trailing newlines,
        and normalize likely random values (memory addresses and UUIDs)
        """
        if not isinstance(s, six.string_types):
            return s

        """
        re.sub matches a regex and replaces it with another. It
        is used to find finmag stamps (Time and date followed by INFO,
        DEBUG, WARNING) and the whole line is replaced with a single
        word.

        The regex replacements are taken from a file if the option
        is passed when py.test is called. Otherwise, the strings
        are not processed
        """
        for regex, replace in six.iteritems(self.parent.sanitize_patterns):
            s = re.sub(regex, replace, s)
        return s


def get_sanitize_patterns(string):
    """
    *Arguments*

    string:  str

        String containing a list of regex-replace pairs as would be
        read from a sanitize config file.

    *Returns*

    A list of (regex, replace) pairs.
    """
    return re.findall('^regex: (.*)$\n^replace: (.*)$',
                         string,
                         flags=re.MULTILINE)
