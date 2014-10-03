import pytest
import os,sys
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

from IPython.nbformat.current import reads

class IPyNbException(Exception):
    """ custom exception for error reporting. """

def pytest_collect_file(path, parent):
    if path.fnmatch("test*.ipynb"):
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

    def __init__(self):
        self.km = KernelManager()
        self.km.start_kernel(stderr=open(os.devnull, 'w'))
        self.kc = self.km.client()
        self.kc.start_channels()
        self.shell = self.kc.shell_channel
        self.shell.execute("pass")
        self.shell.get_msg()

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

            for ws in self.nb.worksheets:
                for cell in ws.cells:
                    if cell.cell_type == "code":
                        yield IPyNbCell(self.name, self, cell_num, cell)
                    cell_num += 1

    def setup(self):
        self.fixture_cell = None
        self.kernel = RunningKernel()

    def teardown(self):
        self.kernel.stop()

class IPyNbCell(pytest.Item):
    def __init__(self, name, parent, cell_num, cell):
        super(IPyNbCell, self).__init__(name, parent)

        self.cell_num = cell_num
        self.cell = cell
        self.cell_description = get_cell_description(self.cell.input)

    def runtest(self):
        self.parent.kernel.restart()
        shell = self.parent.kernel.shell
        
        if self.parent.fixture_cell:
            shell.execute(self.parent.fixture_cell.input, allow_stdin=False)
        msg_id = shell.execute(self.cell.input, allow_stdin=False)
        if self.cell_description.lower().startswith("fixture") or self.cell_description.lower().startswith("setup"):
            self.parent.fixture_cell = self.cell
        timeout = 20
        while True:
            try:
                msg = shell.get_msg(block=True, timeout=timeout)
                if msg.get("parent_header", None) and msg["parent_header"].get("msg_id", None) == msg_id:
                    break
            except Empty:
                raise IPyNbException("Timeout of %d seconds exceeded executing cell: %s" (timeout, self.cell.input))

        reply = msg['content']

        if reply['status'] == 'error':
            raise IPyNbException(self.cell_num, self.cell_description, self.cell.input, '\n'.join(reply['traceback']))

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
