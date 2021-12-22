
import os
import re

import nbformat
from utils import build_nb

pytest_plugins = "pytester"


_ignore_stderr_code = """
def pytest_collectstart(collector):
    if collector.fspath and collector.fspath.ext == '.ipynb':
        collector.skip_compare += ('stderr',)
"""


def test_conf_ignore_stderr(testdir):

    # Setup test config
    testdir.makeconftest(_ignore_stderr_code)

    # Setup notebook with stream outputs
    nb = build_nb([
        "import sys",
        "print('test')",
        "print('error output', file=sys.stderr)",
        "print('test')\nprint('error output', file=sys.stderr)",
    ], mark_run=True)
    nb.cells[1].outputs.append(nbformat.v4.new_output(
        'stream',
        text=u'test\n',
        ))
    nb.cells[2].outputs.append(nbformat.v4.new_output(
        'stream',
        name='stderr',
        text=u'different error output',
        ))
    nb.cells[3].outputs.append(nbformat.v4.new_output(
        'stream',
        text=u'test\n',
        ))
    nb.cells[3].outputs.append(nbformat.v4.new_output(
        'stream',
        name='stderr',
        text=u'different error output',
        ))

    # Write notebook to test dir
    nbformat.write(nb, os.path.join(
        str(testdir.tmpdir), 'test_ignore.ipynb'))

    # Run tests
    result = testdir.runpytest_subprocess('--nbval', '--nbval-current-env', '.')

    # Check tests went off as they should:
    assert result.ret == 0
