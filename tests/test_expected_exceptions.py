import os

import nbformat
import pytest

from utils import build_nb


pytest_plugins = "pytester"


def test_run_raises(testdir):
    # This test uses the testdir fixture from pytester, which is useful for
    # testing pytest plugins. It writes a notebook to a temporary dir
    # and then runs pytest.

    # Setup notebook to test:
    sources = [
        # In [1]:
        "",   # No error produced, when one is expected
        # In [2]:
        "raise ValueError('foo')",   # Wrong ename
        # In [3]:
        "raise ValueError('foo')",   # Wrong evalue
    ]
    # Build unrun notebook:
    nb = build_nb(sources, mark_run=True)

    nb.cells[0].metadata.tags = ['raises-exception']
    nb.cells[0].outputs.append(
        nbformat.v4.new_output(
            'error',
            ename='ValueError',
            evalue='foo',
            traceback=['foobar', 'bob'],  # Should be ignored
        )
    )

    nb.cells[1].metadata.tags = ['raises-exception']
    nb.cells[1].outputs.append(
        nbformat.v4.new_output(
            'error',
            ename='TypeError',   # Expected TypeError, got ValueError
            evalue='foo',
            traceback=['foobar', 'bob'],  # Should be ignored
        )
    )

    nb.cells[2].metadata.tags = ['raises-exception']
    nb.cells[2].outputs.append(
        nbformat.v4.new_output(
            'error',
            ename='ValueError',
            evalue='bar',   # Expected bar, got foo
            traceback=['foobar', 'bob'],  # Should be ignored
        )
    )

    # Write notebook to test dir
    nbformat.write(nb, os.path.join(
        str(testdir.tmpdir), 'test_expcted_exceptions.ipynb'))

    # Run tests
    result = testdir.runpytest_subprocess('--nbval', '--current-env', '-s')
    result.assert_outcomes(failed=3)



def test_unrun_raises(testdir):
    # This test uses the testdir fixture from pytester, which is useful for
    # testing pytest plugins. It writes a notebook to a temporary dir
    # and then runs pytest.

    # Setup notebook to test:
    sources = [
        # In [1]:
        "pass",
    ]
    # Build unrun notebook:
    nb = build_nb(sources, mark_run=False)
    nb.cells[0].metadata.tags = ['raises-exception']

    # Write notebook to test dir
    nbformat.write(nb, os.path.join(
        str(testdir.tmpdir), 'test_expcted_exceptions.ipynb'))

    # Run tests
    result = testdir.runpytest_subprocess('--nbval', '--current-env', '-s')
    result.assert_outcomes(failed=1)
