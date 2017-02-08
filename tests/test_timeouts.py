import os

import nbformat


pytest_plugins = "pytester"


def test_timeouts(testdir):
    # This test uses the testdir fixture from pytester, which is useful for
    # testing pytest plugins. It writes a notebook to a temporary dir
    # and then runs pytest.

    # Note: The test and the notebook are defined together in order to
    # emphasize the close dependence of the test on the structure and
    # content of the notebook

    # Setup notebook to test:
    nb = nbformat.v4.new_notebook()

    cell = nbformat.v4.new_code_cell(
        "from time import sleep")
    nb.cells.append(cell)

    cell = nbformat.v4.new_code_cell(
        "for i in range(100000):\n    sleep(1)\nmyvar = 5")
    nb.cells.append(cell)

    cell = nbformat.v4.new_code_cell(
        "a = 5")
    nb.cells.append(cell)

    cell = nbformat.v4.new_code_cell(
        "print(myvar)")
    nb.cells.append(cell)

    cell = nbformat.v4.new_code_cell(
        "for i in range(1000):\n    sleep(100)")
    nb.cells.append(cell)

    cell = nbformat.v4.new_code_cell(
        "b = 5")
    nb.cells.append(cell)

    # Write notebook to test dir
    nbformat.write(nb, os.path.join(
        str(testdir.tmpdir), 'test_timeouts.ipynb'))

    # Run tests
    result = testdir.inline_run('--nbval', '--current-env', '--nbval-cell-timeout', '5')
    reports = result.getreports('pytest_runtest_logreport')

    # Setup and teardown of cells should have no issues:
    setup_teardown = [r for r in reports if r.when != 'call']
    for r in setup_teardown:
        assert r.passed

    reports = [r for r in reports if r.when == 'call']

    assert len(reports) == 6

    # Import cell should pass:
    assert reports[0].passed

    # First timeout cell should fail, unexpectedly
    assert reports[1].failed and not hasattr(reports[1], 'wasxfail')

    # Normal cell after timeout should pass, but be expected to fail
    assert reports[2].passed and hasattr(reports[2], 'wasxfail')

    # Cell trying to access variable declare after loop in timeout
    # should fail, expectedly (marked skipped)
    assert reports[3].skipped and hasattr(reports[3], 'wasxfail')

    # Second timeout loop should fail, expectedly, and cause all following to fail
    assert reports[4].skipped and hasattr(reports[4], 'wasxfail')
    assert reports[5].skipped and hasattr(reports[5], 'wasxfail')

