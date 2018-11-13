import os

import nbformat
import pytest

from utils import build_nb


pytest_plugins = "pytester"


def test_unrun_raises(testdir):
    # This test uses the testdir fixture from pytester, which is useful for
    # testing pytest plugins. It writes a notebook to a temporary dir
    # and then runs pytest.

    # Setup notebook to test:
    sources = [
        # In [1]:
        "raise ValueError('foo')",
    ]
    # Build unrun notebook:
    nb = build_nb(sources, mark_run=False)

    # Write notebook to test dir
    nbformat.write(nb, os.path.join(
        str(testdir.tmpdir), 'test_expcted_exceptions.ipynb'))

    # Run tests
    result = testdir.inline_run('--nbval', '--current-env', '-s')
    reports = result.getreports('pytest_runtest_logreport')

    # Setup and teardown of cells should have no issues:
    setup_teardown = [r for r in reports if r.when != 'call']
    for r in setup_teardown:
        assert r.passed

    reports = [r for r in reports if r.when == 'call']

    assert len(reports) == 1

    # First cell should fail, unexpectedly
    assert reports[0].failed and not hasattr(reports[0], 'wasxfail')
