import os

import nbformat

import pytest

from utils import build_nb


pytest_plugins = "pytester"

@pytest.mark.parametrize("magic, expected_passes", [
    (r"%dirs", [True]),
    (r"%precision bad", [False]),
    (r"%this_magic_does_not_exist", [False])
])
def test_magics(testdir, magic, expected_passes):
    # Setup notebook to test:
    sources = [
        # In [1]:
        magic,
    ]
    nb = build_nb(sources)

    # Write notebook to test dir
    nbformat.write(nb, os.path.join(
        str(testdir.tmpdir), 'test_magics.ipynb'))

    # Run tests
    result = testdir.inline_run('--nbval-lax', '--current-env', '-s')
    reports = result.getreports('pytest_runtest_logreport')

    # Setup and teardown of cells should have no issues:
    setup_teardown = [r for r in reports if r.when != 'call']
    for r in setup_teardown:
        assert r.passed

    reports = [r for r in reports if r.when == 'call']

    assert len(reports) == len(expected_passes)

    for actual_report, expected_pass in zip(reports, expected_passes):
        assert actual_report.passed is expected_pass
