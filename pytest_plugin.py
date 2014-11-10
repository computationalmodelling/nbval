import pytest
import os
import sys
# For regular expressions:
import re

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


class IPyNbException(Exception):
    """ custom exception for error reporting. """


def pytest_collect_file(path, parent):
    if path.fnmatch("*.ipynb"):
        return IPyNbFile(path, parent)


def get_cell_description(cell_input):
    """Gets cell description

    Cell description is the first line of a cell,
    in one of this formats:

    * single line docstring
    * single line comment
    * function definition
    """
    try:
        first_line = cell_input.split("\n")[0]
        if first_line.startswith(('"', '#', 'def')):
            return first_line.replace('"','').replace("#",'').replace('def ', '').replace("_", " ").strip()
    except:
        pass
    return "no description"

class RunningKernel(object):
    """
    Running a Kernel in IPython, info can be found at:
    http://ipython.org/ipython-doc/stable/development/messaging.html
    """

    def __init__(self):
        # We add the neccesary modules according to the parsenb.py
        # script
        self.km = KernelManager()
        self.km.start_kernel(extra_arguments=['--matplotlib=inline'],
                             stderr=open(os.devnull, 'w'))
        # We need the iopub to read every line in the cells
        try:
            # this procedure seems to work with the newest iPython versions
            self.kc = self.km.client()
            self.kc.start_channels()

            self.iopub = self.kc.iopub_channel
        except:
            self.kc = self.km
            self.kc.start_channels()
            self.iopub = self.kc.sub_channel

        self.shell = self.kc.shell_channel

        # self.shell.execute("pass")
        # self.shell.get_msg()

        # print '============= INITIATING ================='

        # I still dont know if this should go into the IPyNbCell class
        # while True:
        #     try:
        #         print self.iopub.get_msg(timeout=1)
        #     except Empty:
        #         break

    def restart(self):
        self.km.restart_kernel(now=True)

    def stop(self):
        self.kc.stop_channels()
        self.km.shutdown_kernel()
        del self.km


class IPyNbFile(pytest.File):
    def collect(self):
        with self.fspath.open() as f:
            self.nb = reads(f.read(), 'json')

            cell_num = 0

            # We must merge the parsenb code here!
            for ws in self.nb.worksheets:
                for cell in ws.cells:
                    # We need to call the iopub from the setup !
                    # If the cell is code, move to next cell
                    if cell.cell_type == 'code':
                            yield IPyNbCell(self.name, self, cell_num, cell)

                    # Otherwise the cell is an output cell, run it!
                    # try:
                        # This is from the prsenb code:
                        # we must change it according to this script, where
                        # the cell inspection is made by IPyNbCell
                        # outs = run_cell(shell, iopub, cell, t, tshell)
                        # yield?
                    # except Exception as e:
                    #     print "failed to run cell:", repr(e)
                    #     print cell.input

                    # OLD CODE:!!!!
                    # if cell.cell_type == "code":
                    #     yield IPyNbCell(self.name, self, cell_num, cell)
                    cell_num += 1

    def setup(self):
        self.fixture_cell = None
        # Start kernel as usual. We added the
        self.kernel = RunningKernel()

    def teardown(self):
        self.kernel.stop()


class IPyNbCell(pytest.Item):
    def __init__(self, name, parent, cell_num, cell):
        super(IPyNbCell, self).__init__(name, parent)

        self.cell_num = cell_num
        self.cell = cell
        self.cell_description = get_cell_description(self.cell.input)

    # 'Compare outputs' function from the original script
    # We have to integrate this into the main loop
    def compare_outputs(self, test, ref, skip_compare=('png',
                                                       'traceback',
                                                       'latex',
                                                       'prompt_number')):
        for key in ref:
            if key not in test:
                print "missing key: %s != %s" % (test.keys(), ref.keys())
                return False
            elif (key not in skip_compare and self.sanitize(test[key]) !=
                  self.sanitize(ref[key])):
                print bcolors.FAIL + "mismatch %s:" % key + bcolors.ENDC
                print test[key]
                print '  !=  '
                print ref[key]
                print bcolors.OKBLUE + 'DEBUGGING INFO' + bcolors.ENDC
                print '=============='
                # print 'The absolute test string:'
                # print sanitize(test[key])
                # print 'failed to compare with the reference:'
                # print sanitize(ref[key])
                # print '---------------------------------------'
                print "\n\n"
                return False
        return True

    def runtest(self):
        """
        Run all the cell tests in one kernel without restarting.
        It is very common for ipython notebooks to run through assuming a
        single kernel.
        """
        # self.parent.kernel.restart()

        # Get the current shell
        shell = self.parent.kernel.shell
        # Call iopub (TESTING!!)
        iopub = self.parent.kernel.iopub

        """
        if self.parent.fixture_cell:
            shell.execute(self.parent.fixture_cell.input, allow_stdin=False)
        """

        """
        Execute the code from the cell and get the msg_id of the shell process.
        This is the parent header message id for subsequent
        """
        msg_id = shell.execute(self.cell.input,
                               allow_stdin=False)

        """
        if self.cell_description.lower().startswith("fixture") or self.cell_description.lower().startswith("setup"):
            self.parent.fixture_cell = self.cell
        """

        timeout = 2000

        # This list stores the output information for the entire cell
        outs = []

        # Let's try to put this as in the kernel_testing: shell.get_msg outside
        # the while loop and the iopub.get_mesg inside
        shell.get_msg(timeout=timeout)
        
        while True:
            """
            The messages from the cell contain information such
            as input code, outputs generated
            and other messages. We iterate through each message
            until we reach the end of the cell.
            """
            try:
                # Gets one message at a time
                msg = iopub.get_msg(timeout=5.)
                # print '== IOPUB STUFF ==='
                # print msg['content']
                #print 'TYPEEEE'
                #print msg['msg_type']

                # Breaks on the last message
                # if (msg.get("parent_header", None) and
                #         msg["parent_header"].get("msg_id", None) == msg_id):
                #     break
            except Empty:
                # This is not working: ! The code will not be checked
                # if the time is out (when the cell stops to be executed?)
                # raise IPyNbException("Timeout of %d seconds exceeded"
                #                      " executing cell: %s" (timeout,
                #                                             self.cell.input))
                # This is better:
                    break
            """
            We want to compare the outputs of the messages
            to a reference output
            """

            # If the message isn't an output, we don't do anything else with it
            msg_type = msg['msg_type']
            
            # print 'TYPEEE 2:'
            # print msg_type
            if msg_type in ('status', 'pyin'):
                continue
            # elif msg_type == 'clear_output':
            #     outs = []
            #     continue
            # I added the msg_type 'idle' condition (when the cell stops)
            elif (msg_type == 'clear_output' 
                  and msg_type['execution_state'] == 'idle'):
                outs = []
                continue

            reply = msg['content']
            
            out = NotebookNode(output_type=msg_type)

            # Now check what type of output it is
            if msg_type == 'stream':
                out.stream = reply['name']
                out.text = reply['data']
            elif msg_type in ('display_data', 'pyout'):
                out['metadata'] = reply['metadata']
                for mime, data in reply['data'].iteritems():
                    attr = mime.split('/')[-1].lower()
                    attr = attr.replace('+xml', '').replace('plain', 'text')
                    setattr(out, attr, data)
                if msg_type == 'pyout':
                    out.prompt_number = reply['execution_count']
            else:
                print "unhandled iopub msg:", msg_type
            
            # print 'OUT STATUS ========='
            # print outs
            outs.append(out)

        """
        This message is the last message of the cell, which contains no output.
        It only indicates whether the entire cell ran successfully or if there
        was an error.
        """
        reply = msg['content']
        # We have here a dictionary with all the output from a cell !!
        # (we still need the reference)
        # print "Outputs are....\n\n"
        # print outs
        # print "\n\n Reply is..... \n\n"
        # print reply

        # We need to get the reference from the outputs that are already
        # in the notebook
        print '============= REFERENCE ??? ======== \n'
        print self.cell.outputs
        print '\n\n'

        # We need to get the reference from the outputs that are already
        # in the notebook
        print '============= OUTPUT ??? ======== \n'
        print outs
        print '\n\n'


        failed = False
        for out, ref in zip(outs, self.cell.outputs):
            # print '\n This is the output: \n'
            # print out
            # print '\n'
            # print 'This is the reference:\n'
            # print ref
            # print '\n'
            if not self.compare_outputs(out, ref):
                failed = True
        # if failed:
        #     failures += 1
        # else:
        #     successes += 1
        # sys.stdout.write('.')

        # raise NotImplementedError
        
        # if reply['status'] == 'error':
        # Traceback is only when an error is raised (?)
        # We usually get an exception because traceback is not defined
        if failed:  # Use this to make the test fail
            # raise IPyNbException(self.cell_num,
            #                      self.cell_description,
            #                      self.cell.input,
            #                      '\n'.join(reply['traceback']))
            raise IPyNbException(self.cell_num,
                                 self.cell_description,
                                 self.cell.input,
                                 # Here we must put the difference
                                 '\n'.join('FAILED'))


        """
        The pytest exception will be raised if there are any
        errors in the notebook cells. Now we check that
        the outputs produced from running each cell
        matches the outputs in the existing notebook.
        This code is taken from [REF].
        """

    def sanitize(self, s):
        """sanitize a string for comparison.

        fix universal newlines, strip trailing newlines, and normalize likely random values (memory addresses and UUIDs)
        """
        if not isinstance(s, basestring):
            return s

        """
        re.sub matches a regex and replaces it with another. It
        is used to find finmag stamps (Time and date followed by INFO,
        DEBUG, WARNING) and the whole line is replaced with a single
        word.
        """
        s = re.sub(r'\[.*\] INFO:.*', 'FINMAG INFO:', s)
        s = re.sub(r'\[.*\] DEBUG:.*', 'FINMAG DEBUG:', s)
        s = re.sub(r'\[.*\] WARNING:.*', 'FINMAG WARNING:', s)

        """
        Using the same method we strip UserWarnings from matplotlib
        """
        s = re.sub(r'.*/matplotlib/.*UserWarning:.*', 'MATPLOTLIB USERWARNING', s)

        # Also for gmsh information lines
        s = re.sub(r'Info    :.*', 'GMSH INFO', s)

        # normalize newline:
        s = s.replace('\r\n', '\n')

        # ignore trailing newlines (but not space)
        s = s.rstrip('\n')

        # normalize hex addresses:
        s = re.sub(r'0x[a-f0-9]+', '0xFFFFFFFF', s)

        # normalize UUIDs:
        s = re.sub(r'[a-f0-9]{8}(\-[a-f0-9]{4}){3}\-[a-f0-9]{12}', 'U-U-I-D', s)

        return s

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        if isinstance(excinfo.value, IPyNbException):
            return "\n".join([
                "Notebook execution failed",
                "Cell %d: %s\n\n"
                "Input:\n%s\n\n"
                "Traceback:\n%s\n" % excinfo.value.args,
            ])
        else:
            return "pytest plugin exception: %s" % str(excinfo.value)

    def reportinfo(self):
        description = "cell %d" % self.cell_num
        if self.cell_description:
            description += ": " + self.cell_description
        return self.fspath, 0, description
