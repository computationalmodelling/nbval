import os
import sys
from Queue import Empty

try:
    from IPython.kernel import KernelManager
except ImportError:
    from IPython.zmq.blockingkernelmanager import BlockingKernelManager as KernelManager

from IPython.nbformat.current import reads, NotebookNode


def run_cell(shell, iopub, cell, t, tshell):
    """
    Here we will figure out how the timings affect the outputs
    """
    print '\n\n =========== RUNNING CELL for timeout={} ================ \n\n'.format(t)
    shell.execute(cell.input)
    # wait for finish, maximum 20s
    shell.get_msg(timeout=tshell)
    outs = []

    while True:
        try:
            msg = iopub.get_msg(timeout=t)
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


def execute_kernel(nb, t, tshell):
    """
    Load Kernel stuff

    iopub may be necessary to run through the cell
    """
    km = KernelManager()
    km.start_kernel(extra_arguments=['--matplotlib=inline'],
                    stderr=open(os.devnull, 'w'))
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
            iopub.get_msg(timeout=1)
        except Empty:
            break

    """
    Try to print cell by cell
    """
    # Only one worksheet in the current ipython nbs structure
    for cell in nb.worksheets[0].cells:

        # If the cell is code, move to next cell
        if cell.cell_type != 'code':
            continue

        # Otherwise the cell is an output cell, run it!
        try:
            outs = run_cell(shell, iopub, cell, t, tshell)
            print outs
        except Exception as e:
            print "failed to run cell:", repr(e)
            print cell.input

        # Only print the first cell !
        # break


for ipynb in sys.argv[1:]:
        print "testing %s" % ipynb
        with open(ipynb) as f:
            nb = reads(f.read(), 'json')

        for t in [10, 20, 40]:
            execute_kernel(nb, 1, t)
