
import os
import re

import nbformat
from utils import build_nb, add_expected_plaintext_outputs

pytest_plugins = "pytester"


_re_coverage_report_line = re.compile(r'^(\w)\s*(\d+)\s*(\d+)\s*(\d+)%$')


def test_coverage(testdir):

    testdir.makepyfile(
        # Setup file to cover:
        lib="""
            def mysum(a, b):
                return a + b
            def myprod(a, b):
                return a * b
        """,
        # Setup python file to cover mysum function
        test_lib="""
            import lib
            def test_sum():
                assert lib.mysum(1, 3) == 4
                assert lib.mysum("cat", "dog") == "catdog"
                assert lib.mysum(1.5, 2) == 3.5
        """,
    )

    # Setup notebook to cover myprod function
    nb = build_nb([
        "import lib",
        "lib.myprod(1, 3)",
        "lib.myprod(2.5, 2.5)",
        "lib.myprod(2, 'cat')"
    ], mark_run=True)
    add_expected_plaintext_outputs(nb, [
        None, "3", "6.25", "'catcat'"
    ])
    # Write notebook to test dir
    nbformat.write(nb, os.path.join(
        str(testdir.tmpdir), 'test_coverage.ipynb'))

    # Run tests
    result = testdir.runpytest_inprocess('--nbval', '--nbval-current-env', '--cov', '.')

    # Check tests went off as they should:
    assert result.ret == 0

    # Ensure coverage report was generated:
    assert os.path.exists(os.path.join(str(testdir.tmpdir), '.coverage'))

    # Check that all lines were covered:
    result.stdout.fnmatch_lines([
        'lib.py*4*0*100%'
    ])
