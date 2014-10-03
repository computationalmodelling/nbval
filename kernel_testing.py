import os
import sys
from Queue import Empty

try:
    from IPython.kernel import KernelManager
except ImportError:
    from IPython.zmq.blockingkernelmanager import BlockingKernelManager as KernelManager

from IPython.nbformat.current import reads, NotebookNode


def run_cell(shell, iopub, cell):
    """
    Here we will figure out how the timings affect the outputs
    """

    print '\n\n RUNNING CELL \n\n'
    print shell.execute(cell.input)

    # wait for finish, maximum 20s
    shell.get_msg(timeout=1000)
    outs = []

    while True:
        try:
            msg = iopub.get_msg(timeout=1.)
        except Empty:
            break
        msg_type = msg['msg_type']
        if msg_type in ('status', 'pyin'):
            continue
        elif msg_type == 'clear_output':
            outs = []
            continue

        content = msg['content']

        print '\n PRINTING THROUGH THE CELL \n'
        print content

        out = NotebookNode(output_type=msg_type)


def execute_kernel(nb):
    """
    Load Kernel stuff

    iopub may be necessary to run through the cell
    """
    km = KernelManager()
    km.start_kernel(extra_arguments=['--pylab=inline'], stderr=open(os.devnull, 'w'))
    try:
        kc = km.client()
        kc.start_channels()
        iopub = kc.iopub_channel
    except AttributeError:
        # IPython 0.13
        kc = km
        kc.start_channels()
        iopub = kc.sub_channel
    shell = kc.shell_channel

    """
    This part needs revision
    """
    # run %pylab inline, because some notebooks assume this
    # even though they shouldn't
    shell.execute("pass")
    shell.get_msg()
    while True:
        try:
            print iopub.get_msg(timeout=1)
        except Empty:
            break

    """
    Try to print cell by cell
    """
    for cell in nb.worksheets[0].cells:

        # If the cell is code, move to next cell
        if cell.cell_type != 'code':
            continue

        # Otherwise the cell is an output cell, run it!
        try:
            outs = run_cell(shell, iopub, cell)
            print outs
        except Exception as e:
            print "failed to run cell:", repr(e)
            print cell.input



for ipynb in sys.argv[1:]:
        print "testing %s" % ipynb
        with open(ipynb) as f:
            nb = reads(f.read(), 'json')
        execute_kernel(nb)
