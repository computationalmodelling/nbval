"""
pytest ipython plugin modification

Authors: D. Cortes, O. Laslett

"""

import pytest
import os
import sys

# For regular expressions:
import re
# For using a external file with the regex expressions
# to sanitise the outputs
import ConfigParser

try:
    from exceptions import Exception
except:
    pass

wrapped_stdin = sys.stdin
sys.stdin = sys.__stdin__
from IPython.kernel import KernelManager
sys.stdin = wrapped_stdin
try:
    from Queue import Empty
except:
    from queue import Empty

from IPython.nbformat.current import reads, NotebookNode


# Colours for outputs
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
    """
    group = parser.getgroup("general")
    group.addoption('--ipynb', action='store_true',
                    help="Validate IPython notebooks")

    group.addoption('--sanitize_file',
                    help='File with regex expressions to sanitize '
                         'the outputs. This option only works when '
                         'the --ipynb flag is passed to py.test')


# def pytest_configure(config):
#     """ called after command line options have been parsed
#         and all plugins and initial conftest files been loaded.
#     """
#     if config.option.sanitise_file:
#         if not config.option.ipynb:
#             raise NameError('ERROR: Config file without --ipynb flag')
#         else:


def pytest_collect_file(path, parent):
    """
    Collect iPython notebooks using the specified pytest hook
    """
    if path.fnmatch("*.ipynb") and parent.config.option.ipynb:
        return IPyNbFile(path, parent)


class RunningKernel(object):
    """
    Running a Kernel in IPython, info can be found at:
    http://ipython.org/ipython-doc/stable/development/messaging.html
    """

    def __init__(self):
        # Start an ipython kernel
        self.km = KernelManager()
        self.km.start_kernel(extra_arguments=['--matplotlib=inline'],
                             stderr=open(os.devnull, 'w'))
        # We need iopub to read every line in the cells
        """
        http://ipython.org/ipython-doc/stable/development/messaging.html

        IOPub: this socket is the 'broadcast channel' where the kernel
        publishes all side effects (stdout, stderr, etc.) as well as the
        requests coming from any client over the shell socket and its
        own requests on the stdin socket. There are a number of actions
        in Python which generate side effects: print() writes to sys.stdout,
        errors generate tracebacks, etc. Additionally, in a multi-client
        scenario, we want all frontends to be able to know what each other
        has sent to the kernel (this can be useful in collaborative scenarios,
        for example). This socket allows both side effects and the information
        about communications taking place with one client over the shell
        channel to be made available to all clients in a uniform manner.

        Check: stderr and stdout in the NbCellError function at the end
        (if we get an error, check the msg_type and make the test to fail)
        """
        try:
            # This procedure seems to work with the newest iPython versions
            self.kc = self.km.client()
            self.kc.start_channels()
            self.iopub = self.kc.iopub_channel
        except:
            # Otherwise load it as
            self.kc = self.km
            self.kc.start_channels()
            self.iopub = self.kc.sub_channel

        # Start the shell to execute cels in the notebook (send messages?)
        self.shell = self.kc.shell_channel

    # These options are in case we wanted to restart the nb every time
    # it is executed a certain task
    def restart(self):
        self.km.restart_kernel(now=True)

    def stop(self):
        self.kc.stop_channels()
        self.km.shutdown_kernel()
        del self.km


class IPyNbFile(pytest.File):
    # Read through the specified notebooks and load the data
    # (which is in json format)
    def collect(self):
        with self.fspath.open() as f:
            self.nb = reads(f.read(), 'json')

            # Start the cell count
            cell_num = 0

            # Currently there is only 1 worksheet (it seems in newer versions
            # of iPython, they are going to get rid of this option)
            # For every worksheet, read every cell associated to it
            for ws in self.nb.worksheets:
                for cell in ws.cells:
                    # Skip the cells that have text, headings or related stuff
                    # Only test code cells
                    if cell.cell_type == 'code':
                        # If the code is a notebook magic cell, do not run
                        # i.e. cell code starts with '%%'
                        # Also ignore the cells that start with the
                        # comment string PYTEST_VALIDATE_IGNORE_OUTPUT
                        if not (cell.input.startswith('%%') or
                                cell.input.startswith(r'# PYTEST_VALIDATE_IGNORE_OUTPUT') or
                                cell.input.startswith(r'#PYTEST_VALIDATE_IGNORE_OUTPUT')):

                            yield IPyNbCell(self.name, self, cell_num, cell)

                        else:
                            # Skipped cells will not be counted
                            continue

                    # Update 'code' cell count
                    cell_num += 1

    # Start the iPython kernel and the sanitize instance, using the
    # ConfigParser library, if the option was selected in the input
    # These are parent options of the IPyNbCell class
    # The self.Config is used in the sanitize function of the
    # IPyNbCell class
    def setup(self):
        self.fixture_cell = None
        self.kernel = RunningKernel()

        try:
            self.sanitize_file = self.parent.config.option.sanitize_file
            self.Config = ConfigParser.ConfigParser()
            # When reading the file, the sections are registered.
            # Currently, the section names are not meaningful
            self.Config.read(self.sanitize_file)
        except:
            self.sanitize_file = None

    def teardown(self):
        self.kernel.stop()


class IPyNbCell(pytest.Item):
    def __init__(self, name, parent, cell_num, cell):
        super(IPyNbCell, self).__init__(name, parent)

        # Get the numbers
        self.cell_num = cell_num
        self.cell = cell

        #
        self.comparisons = None

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
                                                       'png',
                                                       'traceback',
                                                       'latex',
                                                       'prompt_number')):
        self.comparisons = []

        for key in ref:
            # Check that the output types match
            if key not in test:

                self.comparisons.append(bcolors.FAIL
                                        + "missing key: %s != %s"
                                        % (test.keys(), ref.keys())
                                        + bcolors.ENDC)
                return False
            # Check that the output types are not in the skip_compare list,
            # sanitise the output line and compare them
            elif key not in skip_compare:
                if (self.sanitize(test[key]) !=
                        self.sanitize(ref[key])):

                    self.comparisons.append(bcolors.OKBLUE
                                            + " mismatch '%s'\n" % key
                                            + bcolors.FAIL
                                            + "<<<<<<<<<<<< Newly computed (test) output:"
                                            + bcolors.ENDC)
                    self.comparisons.append(test[key])
                    self.comparisons.append(bcolors.FAIL
                                            + '============ disagrees with reference output from ipynb file:  '
                                            + bcolors.ENDC)
                    self.comparisons.append(ref[key])
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
        # self.parent.kernel.restart()

        # Get the current shell for executing code cells
        shell = self.parent.kernel.shell
        # Call iopub to get the messages from the executions
        iopub = self.parent.kernel.iopub

        # Execute the code from the current cell and get the msg_id of the
        #  shell process.
        msg_id = shell.execute(self.cell.input,
                               allow_stdin=False)

        # Time for the reply of the cell execution
        timeout = 2000

        # This list stores the output information for the entire cell
        outs = []

        # Wait for the execution reply (we can see this in the msg_type)
        # This execution produces a dictionary where a status string can be
        # obtained: 'ok' OR 'error' OR 'abort'
        # We can also get how many cells have been executed
        # until here, with the 'execution_count' entry
        shell.get_msg(timeout=timeout)

        while True:
            """
            The messages from the cell contain information such
            as input code, outputs generated
            and other messages. We iterate through each message
            until we reach the end of the cell.
            """
            try:
                # Get one message at a time, per code block inside
                # the cell
                msg = iopub.get_msg(timeout=1.)

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

            # Firstly, get the msg type from the cell to know if
            # the output comes from a code
            # It seems that the type 'stream' is irrelevant
            msg_type = msg['msg_type']

            # REF:
            # pyin: To let all frontends know what code is being executed at
            # any given time, these messages contain a re-broadcast of the code
            # portion of an execute_request, along with the execution_count.
            if msg_type in ('status', 'pyin'):
                continue

            # If there is no more output, conitnue with the executions
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
            elif (msg_type == 'clear_output'
                  and msg_type['execution_state'] == 'idle'):
                outs = []
                continue

            # WE COULD ADD HERE a condition for the 'pyerr' message type
            # Making the test to fail

            """
            Now we get the reply from the piece of code executed
            and analyse the outputs
            """
            reply = msg['content']
            out = NotebookNode(output_type=msg_type)

            # Now check what type of output it is
            if msg_type == 'stream':
                out.stream = reply['name']
                out.text = reply['data']
            elif msg_type in ('display_data', 'pyout'):
                # REF:
                # data and metadata are identical to a display_data message.
                # the object being displayed is that passed to the display
                #  hook, i.e. the *result* of the execution.
                out['metadata'] = reply['metadata']
                for mime, data in reply['data'].iteritems():
                    attr = mime.split('/')[-1].lower()
                    attr = attr.replace('+xml', '').replace('plain', 'text')
                    setattr(out, attr, data)
                if msg_type == 'pyout':
                    out.prompt_number = reply['execution_count']
            else:
                print("unhandled iopub msg:", msg_type)

            outs.append(out)

        """
        This message is the last message of the cell, which contains no output.
        It only indicates whether the entire cell ran successfully or if there
        was an error.
        """
        reply = msg['content']

        failed = False

        # Compare if the outputs have the same number of lines
        # and throw an error if it fails
        if len(outs) != len(self.cell.outputs):
            self.comparisons = []
            self.comparisons.append(bcolors.FAIL
                                    + 'Mismatch number of outputs'
                                    + ' in cell'
                                    + bcolors.ENDC)

            failed = True
        # If the outputs are the same, compare them line by line
        else:
            for out, ref in zip(outs, self.cell.outputs):
                if not self.compare_outputs(out, ref):
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
                              self.cell.input,
                              # Here we must put the traceback output:
                              '\n'.join(self.comparisons))

    def sanitize(self, s):
        """sanitize a string for comparison.

        fix universal newlines, strip trailing newlines,
        and normalize likely random values (memory addresses and UUIDs)
        """
        if not isinstance(s, basestring):
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
        if self.parent.sanitize_file:
            for sec_name in self.parent.Config.sections():
                s = re.sub(self.parent.Config.get(sec_name, 'regex'),
                           self.parent.Config.get(sec_name, 'replace'),
                           s)

        # normalize newline:
        s = s.replace('\r\n', '\n')

        # ignore trailing newlines (but not space)
        s = s.rstrip('\n')

        return s
