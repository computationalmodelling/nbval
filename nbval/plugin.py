"""
pytest ipython plugin modification

Authors: D. Cortes, O. Laslett, T. Kluyver, H. Fangohr, V.T. Fauske

"""

from __future__ import print_function

# import the pytest API
import pytest
import sys
import re
import hashlib
import warnings
from collections import OrderedDict, defaultdict

# for python 3 compatibility
import six

try:
    from Queue import Empty
except:
    from queue import Empty

# for reading notebook files
import nbformat
from nbformat import NotebookNode

# Kernel for running notebooks
from .kernel import RunningKernel, CURRENT_ENV_KERNEL_NAME


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
    def __init__(self, cell_num, msg, source, traceback=None, *args, **kwargs):
        self.cell_num = cell_num
        super(NbCellError, self).__init__(msg, *args, **kwargs)
        self.source = source
        self.inner_traceback = traceback


def pytest_addoption(parser):
    """
    Adds the --nbval option flag for py.test.

    Adds an optional flag to pass a config file with regex
    expressions to sanitise the outputs
    Only will work if the --nbval flag is present

    This is called by the pytest API
    """
    group = parser.getgroup("general")
    group.addoption('--nbval', action='store_true',
                    help="Validate Jupyter notebooks")

    group.addoption('--nbval-lax', action='store_true',
                    help="Run Jupyter notebooks, only validating output on "
                         "cells marked with # NBVAL_CHECK_OUTPUT")

    group.addoption('--sanitize-with',
                    help='File with regex expressions to sanitize '
                         'the outputs. This option only works when '
                         'the --nbval flag is passed to py.test')

    group.addoption('--current-env', action='store_true',
                    help='Force test execution to use a python kernel in '
                         'the same enviornment that py.test was '
                         'launched from.')

    group.addoption('--nbval-cell-timeout', action='store', default=2000,
                    type=float,
                    help='Timeout for cell execution, in seconds.')

    term_group = parser.getgroup("terminal reporting")
    term_group._addoption(
        '--nbdime', action='store_true',
        help="view failed nbval cells with nbdime.")


def pytest_configure(config):
    if config.option.nbdime:
        from .nbdime_reporter import NbdimeReporter
        reporter = NbdimeReporter(config, sys.stdout)
        config.pluginmanager.register(reporter, 'nbdimereporter')


def pytest_collect_file(path, parent):
    """
    Collect IPython notebooks using the specified pytest hook
    """
    opt = parent.config.option
    if (opt.nbval or opt.nbval_lax) and path.fnmatch("*.ipynb"):
        return IPyNbFile(path, parent)



comment_markers = {
    'PYTEST_VALIDATE_IGNORE_OUTPUT': ('check', False),  # For backwards compatibility
    'NBVAL_IGNORE_OUTPUT': ('check', False),
    'NBVAL_CHECK_OUTPUT': 'check',
    'NBVAL_RAISES_EXCEPTION': 'check_exception',
    'NBVAL_SKIP': 'skip',
}

metadata_tags = {
    k.lower().replace('_', '-'): v
    for (k, v) in comment_markers.items()
}


def find_comment_markers(cellsource):
    """Look through the cell source for comments which affect nbval's behaviour

    Yield an iterable of ``(MARKER_TYPE, True)``.
    """
    found = {}
    for line in cellsource.splitlines():
        line = line.strip()
        if line.startswith('#'):
            # print("Found comment in '{}'".format(line))
            comment = line.lstrip('#').strip()
            if comment in comment_markers:
                # print("Found marker {}".format(comment))
                marker = comment_markers[comment]
                if not isinstance(marker, tuple):
                    # If not an explicit tuple ('option', True/False),
                    # imply ('option', True)
                    marker = (marker, True)
                marker_type = marker[0]
                if marker_type in found:
                    warnings.warn(
                        "Conflicting comment markers found, using the latest: "
                        " %s VS %s" %
                        (found[marker_type], comment))
                found[marker_type] = comment
                yield marker


def find_metadata_tags(cell_metadata):
    tags = cell_metadata.get('tags', None)
    if tags is None:
        return
    elif not isinstance(tags, list):
        warnings.warn("Cell tags is not a list, ignoring.")
        return
    found = {}
    for tag in tags:
        if tag in metadata_tags:
            marker = metadata_tags[tag]
            if not isinstance(marker, tuple):
                # If not an explicit tuple ('option', True/False),
                # imply ('option', True)
                marker = (marker, True)
            marker_type = marker[0]
            if marker_type in found:
                warnings.warn(
                    "Conflicting metadata tags found, using the latest: "
                    " %s VS %s" %
                    (found[marker_type], tag))
            found[marker_type] = tag
            yield marker


class Dummy:
    """Needed to use xfail for our tests"""
    def __init__(self):
        self.__globals__ = {}


class IPyNbFile(pytest.File):
    """
    This class represents a pytest collector object.
    A collector is associated with an ipynb file and collects the cells
    in the notebook for testing.
    yields pytest items that are required by pytest.
    """
    def __init__(self, *args, **kwargs):
        super(IPyNbFile, self).__init__(*args, **kwargs)
        config = self.parent.config
        self.sanitize_patterns = OrderedDict()  # Filled in setup_sanitize_patterns()
        self.compare_outputs = not config.option.nbval_lax
        self.timed_out = False
        self.skip_compare = (
            'metadata',
            'traceback',
            #'text/latex',
            'prompt_number',
            'stdout',
            'stream',
            'name',
            'execution_count',
        )
        if not config.option.nbdime:
            self.skip_compare = self.skip_compare + ('image/png', 'image/jpeg')

    kernel = None

    def setup(self):
        """
        Called by pytest to setup the collector cells in .
        Here we start a kernel and setup the sanitize patterns.
        """

        if self.parent.config.option.current_env:
            kernel_name = CURRENT_ENV_KERNEL_NAME
        else:
            kernel_name = self.nb.metadata.get(
                'kernelspec', {}).get('name', 'python')
        self.kernel = RunningKernel(kernel_name)
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

    def get_kernel_message(self, timeout=None, stream='iopub'):
        """
        Gets a message from the iopub channel of the notebook kernel.
        """
        return self.kernel.get_message(stream, timeout=timeout)

    # Read through the specified notebooks and load the data
    # (which is in json format)
    def collect(self):
        """
        The collect function is required by pytest and is used to yield pytest
        Item objects. We specify an Item for each code cell in the notebook.
        """

        self.nb = nbformat.read(str(self.fspath), as_version=4)

        # Start the cell count
        cell_num = 0

        # Iterate over the cells in the notebook
        for cell in self.nb.cells:
            # Skip the cells that have text, headings or related stuff
            # Only test code cells
            if cell.cell_type == 'code':
                # The cell may contain a comment indicating that its output
                # should be checked or ignored. If it doesn't, use the default
                # behaviour. The --nbval option checks unmarked cells.
                with warnings.catch_warnings(record=True) as ws:
                    options = defaultdict(bool, find_metadata_tags(cell.metadata))
                    comment_opts = dict(find_comment_markers(cell.source))
                    if set(comment_opts.keys()) & set(options.keys()):
                        warnings.warn(
                            "Overlapping options from comments and metadata, "
                            "using options from comments: %s" %
                            str(set(comment_opts.keys()) & set(options.keys())))
                    for w in ws:
                        self.parent.config.warn(
                            "C1",
                            w.message,
                            '%s:Cell %d' % (
                                getattr(self, "fspath", None),
                                cell_num))
                options.update(comment_opts)
                options.setdefault('check', self.compare_outputs)
                yield IPyNbCell('Cell ' + str(cell_num), self, cell_num,
                                cell, options)

                # Update 'code' cell count
                cell_num += 1

    def teardown(self):
        if self.kernel is not None and self.kernel.is_alive():
            self.kernel.stop()


class IPyNbCell(pytest.Item):
    def __init__(self, name, parent, cell_num, cell, options):
        super(IPyNbCell, self).__init__(name, parent)

        # Store reference to parent IPynbFile so that we have access
        # to the running kernel.
        self.parent = parent
        self.cell_num = cell_num
        self.cell = cell
        self.test_outputs = None
        self.options = options
        self.config = parent.parent.config
        self.output_timeout = 5
        # _pytest.skipping assumes all pytest.Item have this attribute:
        self.obj = Dummy()

    """ *****************************************************
        *****************  TESTING FUNCTIONS  ***************
        ***************************************************** """

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        exc = excinfo.value
        if isinstance(exc, NbCellError):
            msg_items = [
                bcolors.FAIL + "Notebook cell execution failed" + bcolors.ENDC]
            formatstring = (
                bcolors.OKBLUE + "Cell %d: %s\n\n" +
                "Input:\n" + bcolors.ENDC + "%s\n")
            msg_items.append(formatstring % (
                exc.cell_num,
                str(exc),
                exc.source
            ))
            if exc.inner_traceback:
                msg_items.append((
                    bcolors.OKBLUE + "Traceback:%s" + bcolors.ENDC) %
                    exc.inner_traceback)
            return "\n".join(msg_items)
        else:
            return "pytest plugin exception: %s" % str(exc)

    def reportinfo(self):
        description = "cell %d" % self.cell_num
        return self.fspath, 0, description

    def compare_outputs(self, test, ref, skip_compare=None):
        # Use stored skips unless passed a specific value
        skip_compare = skip_compare or self.parent.skip_compare

        # For every different key, we will store the outputs in a
        # single string, in a dictionary with the same keys
        # At the end, every dictionary entry will be compared
        # We skip the unimportant keys in the 'skip_compare' list
        #
        # We concatenate the outputs because the ipython notebook produces
        # them in a random number of dictionaries. So, it is easier
        # to compare only one chunk of data
        testing_outs = defaultdict(str)
        reference_outs = defaultdict(str)

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
                                reference_outs[data_key] += self.sanitize(reference[key][data_key])


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
                        reference_outs[key] += self.sanitize(reference[key])

        # the same for the testing outputs (the cells that are being executed)
        # display_data cells were already processed! (see the execution loop)
        for testing in test:
            for key in testing.keys():
                if key not in skip_compare:
                    if key == 'data':
                        for data_key in testing[key].keys():
                            # Filter the keys in the SUB-dictionary again
                            if data_key not in skip_compare:
                                testing_outs[data_key] += self.sanitize(testing[key][data_key])
                    else:
                        testing_outs[key] += self.sanitize(testing[key])

        # The traceback from the comparison will be stored here.
        self.comparison_traceback = []

        for key in reference_outs.keys():

            # Check if they have the same keys
            if key not in testing_outs.keys():
                self.comparison_traceback.append(
                    bcolors.FAIL
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

                self.comparison_traceback.append(
                    bcolors.OKBLUE
                    + " mismatch '%s'\n" % key
                    + bcolors.FAIL
                    + "<<<<<<<<<<<< Reference output from ipynb file:"
                    + bcolors.ENDC)
                self.comparison_traceback.append(_trim_base64(reference_outs[key]))
                self.comparison_traceback.append(
                    bcolors.FAIL
                    + '============ disagrees with newly computed (test) output:  '
                    + bcolors.ENDC)
                self.comparison_traceback.append(_trim_base64(testing_outs[str(key)]))
                self.comparison_traceback.append(
                    bcolors.FAIL
                    + '>>>>>>>>>>>>'
                    + bcolors.ENDC)

                return False
        return True


    """ *****************************************************
        ***************************************************** """

    def setup(self):
        if self.parent.timed_out:
            # xfail(condition, reason=None, run=True, raises=None, strict=False)
            xfail_mark = pytest.mark.xfail(
                True,
                reason='Previous cell timed out, expected cell to fail'
            )
            self.add_marker(xfail_mark)


    def await_idle(self, parent_id):
        """Poll the iopub stream until an idle message is received for the given parent ID"""
        while True:
            try:
                # Get a message from the kernel iopub channel
                msg = self.parent.get_kernel_message(timeout=self.output_timeout)

            except Empty:
                self.parent.kernel.stop()
                raise RuntimeError('Timed out waiting for idle kernel!')
            if msg['parent_header'].get('msg_id') != parent_id:
                continue
            if msg['msg_type'] == 'status':
                if msg['content']['execution_state'] == 'idle':
                    break


    def raise_cell_error(self, message, *args, **kwargs):
        raise NbCellError(self.cell_num, message, self.cell.source, *args, **kwargs)


    def runtest(self):
        """
        Run test is called by pytest for each of these nodes that are
        collected i.e. a notebook cell. Runs all the cell tests in one
        kernel without restarting.  It is very common for ipython
        notebooks to run through assuming a single kernel.  The cells
        are tested that they execute without errors and that the
        output matches the output stored in the notebook.

        """
        # Simply skip cell if configured to
        if self.options['skip']:
            pytest.skip()

        kernel = self.parent.kernel
        if not kernel.is_alive():
            raise RuntimeError("Kernel dead on test start")

        # Execute the code in the current cell in the kernel. Returns the
        # message id of the corresponding response from iopub.
        msg_id = kernel.execute_cell_input(
            self.cell.source, allow_stdin=False)

        # Timeout for the cell execution
        # after code is sent for execution, the kernel sends a message on
        # the shell channel. Timeout if no message received.
        timeout = self.config.option.nbval_cell_timeout
        timed_out_this_run = False

        # Poll the shell channel to get a message
        while True:
            try:
                msg = self.parent.get_kernel_message(stream='shell',
                                                     timeout=timeout)
            except Empty:
                # Try to interrupt kernel, as this will give us traceback:
                kernel.interrupt()
                self.parent.timed_out = True
                timed_out_this_run = True
                break

            # Is this the message we are waiting for?
            if msg['parent_header'].get('msg_id') == msg_id:
                if msg['content']['status'] == 'aborted':
                    # This should not occur!
                    raise RuntimeError('Kernel aborted execution request')
                break
            else:
                continue

        # This list stores the output information for the entire cell
        outs = []
        # TODO: Only store if comparing with nbdime, to save on memory usage
        self.test_outputs = outs

        # Now get the outputs from the iopub channel
        while True:
            # The iopub channel broadcasts a range of messages. We keep reading
            # them until we find the message containing the side-effects of our
            # code execution.
            try:
                # Get a message from the kernel iopub channel
                msg = self.parent.get_kernel_message(timeout=self.output_timeout)

            except Empty:
                # This is not working: ! The code will not be checked
                # if the time is out (when the cell stops to be executed?)
                # Halt kernel here!
                kernel.stop()
                if timed_out_this_run:
                    self.raise_cell_error(
                        "Timeout of %g seconds exceeded while executing cell."
                        " Failed to interrupt kernel in %d seconds, so "
                        "failing without traceback." %
                            (timeout, self.output_timeout),
                    )
                else:
                    self.parent.timed_out = True
                    self.raise_cell_error(
                        "Timeout of %d seconds exceeded waiting for output." %
                            self.output_timeout,
                    )



            # now we must handle the message by checking the type and reply
            # info and we store the output of the cell in a notebook node object
            msg_type = msg['msg_type']
            reply = msg['content']
            out = NotebookNode(output_type=msg_type)

            # Is the iopub message related to this cell execution?
            if msg['parent_header'].get('msg_id') != msg_id:
                continue

            # When the kernel starts to execute code, it will enter the 'busy'
            # state and when it finishes, it will enter the 'idle' state.
            # The kernel will publish state 'starting' exactly
            # once at process startup.
            if msg_type == 'status':
                if reply['execution_state'] == 'idle':
                    break
                else:
                    continue

            # execute_input: To let all frontends know what code is
            # being executed at any given time, these messages contain a
            # re-broadcast of the code portion of an execute_request,
            # along with the execution_count.
            elif msg_type == 'execute_input':
                continue

            # com? execute reply?
            elif msg_type.startswith('comm'):
                continue
            elif msg_type == 'execute_reply':
                continue

            # This message type is used to clear the output that is
            # visible on the frontend
            # elif msg_type == 'clear_output':
            #     outs = []
            #     continue


            # elif (msg_type == 'clear_output'
            #       and msg_type['execution_state'] == 'idle'):
            #     outs = []
            #     continue

            # 'execute_result' is equivalent to a display_data message.
            # The object being displayed is passed to the display
            # hook, i.e. the *result* of the execution.
            # The only difference is that 'execute_result' has an
            # 'execution_count' number which does not seems useful
            # (we will filter it in the sanitize function)
            #
            # When the reply is display_data or execute_result,
            # the dictionary contains
            # a 'data' sub-dictionary with the 'text' AND the 'image/png'
            # picture (in hexadecimal). There is also a 'metadata' entry
            # but currently is not of much use, sometimes there is information
            # as height and width of the image (CHECK the documentation)
            # Thus we iterate through the keys (mimes) 'data' sub-dictionary
            # to obtain the 'text' and 'image/png' information
            elif msg_type in ('display_data', 'execute_result'):
                out['metadata'] = reply['metadata']
                out['data'] = {}
                for mime, data in six.iteritems(reply['data']):
                    # This could be useful for reference or backward compatibility
                    #     attr = mime.split('/')[-1].lower()
                    #     attr = attr.replace('+xml', '').replace('plain', 'text')
                    #     setattr(out, attr, data)

                    # Return the relevant entries from data:
                    # plain/text, image/png, execution_count, etc
                    # We could use a mime types list for this (MAYBE)
                    out.data[mime] = data
                outs.append(out)

                if msg_type == 'execute_result':
                    out.execution_count = reply['execution_count']


            # if the message is a stream then we store the output
            elif msg_type == 'stream':
                out.stream = reply['name']
                out.text = reply['text']
                outs.append(out)


            # if the message type is an error then an error has occurred during
            # cell execution. Therefore raise a cell error and pass the
            # traceback information.
            elif msg_type == 'error':
                # Store error in output first
                out['ename'] = reply['ename']
                out['evalue'] = reply['evalue']
                out['traceback'] = reply['traceback']
                outs.append(out)
                if not self.options['check_exception']:
                    # Ensure we flush iopub before raising error
                    self.await_idle(msg_id)
                    traceback = '\n' + '\n'.join(reply['traceback'])
                    if out['ename'] == 'KeyboardInterrupt' and self.parent.timed_out:
                        msg = "Timeout of %g seconds exceeded executing cell" % timeout
                    else:
                        msg = "Cell execution caused an exception"
                    self.raise_cell_error(msg, traceback)

            # any other message type is not expected
            # should this raise an error?
            else:
                print("unhandled iopub msg:", msg_type)

        # Compare if the outputs have the same number of lines
        # and throw an error if it fails
        # if len(outs) != len(self.cell.outputs):
        #     self.diff_number_outputs(outs, self.cell.outputs)
        #     failed = True
        failed = False
        if self.options['check']:
            if not self.compare_outputs(outs, self.cell.outputs):
                failed = True

        # If the comparison failed then we raise an exception.
        if failed:
            # The traceback containing the difference in the outputs is
            # stored in the variable comparison_traceback
            self.raise_cell_error(
                "Cell outputs differ",
                # Here we must put the traceback output:
                '\n'.join(self.comparison_traceback),
            )


    def sanitize_outputs(self, outputs, skip_sanitize=('metadata',
                                                       'traceback',
                                                       'text/latex',
                                                       'prompt_number',
                                                       'stdout',
                                                       'stream',
                                                       'output_type',
                                                       'name',
                                                       'execution_count'
                                                       )):
        sanitized_outputs = []
        for output in outputs:
            sanitized = {}
            for key in output.keys():
                if key in skip_sanitize:
                    sanitized[key] = output[key]
                else:
                    if key == 'data':
                        sanitized[key] = {}
                        for data_key in output[key].keys():
                            # Filter the keys in the SUB-dictionary again
                            if data_key in skip_sanitize:
                                sanitized[key][data_key] = output[key][data_key]
                            else:
                                sanitized[key][data_key] = self.sanitize(output[key][data_key])

                    # Otherwise, just create a normal dictionary entry from
                    # one of the keys of the dictionary
                    else:
                        # Create the dictionary entries on the fly, from the
                        # existing ones to be compared
                        sanitized[key] = self.sanitize(output[key])
            sanitized_outputs.append(nbformat.from_dict(sanitized))
        return sanitized_outputs

    def sanitize(self, s):
        """sanitize a string for comparison.
        """
        if not isinstance(s, six.string_types):
            return s

        """
        re.sub matches a regex and replaces it with another.
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


def hash_string(s):
    return hashlib.md5(s.encode("utf8")).hexdigest()

_base64 = re.compile(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', re.MULTILINE | re.UNICODE)


def _trim_base64(s):
    """Trim and hash base64 strings"""
    if len(s) > 64 and _base64.match(s.replace('\n', '')):
        h = hash_string(s)
        s = '%s...<snip base64, md5=%s...>' % (s[:8], h[:16])
    return s
