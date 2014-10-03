#!/usr/bin/env python
"""
simple example script for running and testing notebooks.

Usage: `parsenb.py foo.ipynb [bar.ipynb [...]]`

Each cell is submitted to the kernel, and the outputs are compared with those stored in the notebook.
"""

import os,sys,time
import base64
import re

from collections import defaultdict
from Queue import Empty

try:
    from IPython.kernel import KernelManager
except ImportError:
    from IPython.zmq.blockingkernelmanager import BlockingKernelManager as KernelManager

from IPython.nbformat.current import reads, NotebookNode


def compare_png(a64, b64):
    """compare two b64 PNGs (incomplete)"""
    try:
        import Image
    except ImportError:
        pass
    adata = base64.decodestring(a64)
    bdata = base64.decodestring(b64)
    return True

def sanitize(s):
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


def consolidate_outputs(outputs):
    """consolidate outputs into a summary dict (incomplete)"""
    data = defaultdict(list)
    data['stdout'] = ''
    data['stderr'] = ''

    for out in outputs:
        if out.type == 'stream':
            data[out.stream] += out.text
        elif out.type == 'pyerr':
            data['pyerr'] = dict(ename=out.ename, evalue=out.evalue)
        else:
            for key in ('png', 'svg', 'latex', 'html', 'javascript', 'text', 'jpeg',):
                if key in out:
                    data[key].append(out[key])
    return data


def compare_outputs(test, ref, skip_compare=('png', 'traceback', 'latex', 'prompt_number')):
    for key in ref:
        if key not in test:
            print "missing key: %s != %s" % (test.keys(), ref.keys())
            return False
        elif key not in skip_compare and sanitize(test[key]) != sanitize(ref[key]):
            print bcolors.FAIL + "mismatch %s:" % key + bcolors.ENDC
            print test[key]
            print '  !=  '
            print ref[key]
            print bcolors.OKBLUE + 'DEBUGGING INFO' + bcolors.ENDC
            print '=============='
            print 'The absolute test string:'
            print sanitize(test[key])
            print 'failed to compare with the reference:'
            print sanitize(ref[key])
            print '---------------------------------------'
            print "\n\n"
            return False
    return True


def run_cell(shell, iopub, cell):
    # print cell.input
    shell.execute(cell.input)
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
        # print msg_type, content
        out = NotebookNode(output_type=msg_type)

        if msg_type == 'stream':
            out.stream = content['name']
            out.text = content['data']
        elif msg_type in ('display_data', 'pyout'):
            out['metadata'] = content['metadata']
            for mime, data in content['data'].iteritems():
                attr = mime.split('/')[-1].lower()
                # this gets most right, but fix svg+html, plain
                attr = attr.replace('+xml', '').replace('plain', 'text')
                setattr(out, attr, data)
            if msg_type == 'pyout':
                out.prompt_number = content['execution_count']
        elif msg_type == 'pyerr':
            out.ename = content['ename']
            out.evalue = content['evalue']
            out.traceback = content['traceback']
        else:
            print "unhandled iopub msg:", msg_type

        outs.append(out)
    return outs


def test_notebook(nb):
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

    # run %pylab inline, because some notebooks assume this
    # even though they shouldn't
    shell.execute("pass")
    shell.get_msg()
    while True:
        try:
            iopub.get_msg(timeout=1)
        except Empty:
            break

    successes = 0
    failures = 0
    errors = 0
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type != 'code':
                continue
            try:
                outs = run_cell(shell, iopub, cell)
            except Exception as e:
                print "failed to run cell:", repr(e)
                print cell.input
                errors += 1
                continue

            failed = False
            for out, ref in zip(outs, cell.outputs):
                # print '\n This is the output: \n'
                # print out
                # print '\n'
                # print 'This is the reference:\n'
                # print ref
                # print '\n'
                if not compare_outputs(out, ref):
                    failed = True
            if failed:
                failures += 1
            else:
                successes += 1
            sys.stdout.write('.')

    print
    print "tested notebook %s" % nb.metadata.name
    print bcolors.OKGREEN + "    %3i cells successfully replicated" % + successes + bcolors.ENDC
    if failures:
        print bcolors.FAIL + "    %3i cells mismatched output" % failures + bcolors.ENDC
    if errors:
        print bcolors.WARNING + "    %3i cells failed to complete" % errors + bcolors.ENDC
    kc.stop_channels()
    km.shutdown_kernel()
    del km


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


if __name__ == '__main__':
    for ipynb in sys.argv[1:]:
        print "testing %s" % ipynb
        with open(ipynb) as f:
            nb = reads(f.read(), 'json')
        test_notebook(nb)
