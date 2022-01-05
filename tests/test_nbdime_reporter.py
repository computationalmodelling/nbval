
from utils import build_nb, add_expected_plaintext_outputs

import nbdime
import nbformat
import os


def test_nbdime(testdir, mocker):

    # Make a test notebook where output doesn't match input
    nb = build_nb(["1+1", "1+1"], mark_run=True)
    add_expected_plaintext_outputs(nb, ["2", "3"])
    # Write notebook to test dir
    filename = 'test_nbdime.ipynb'
    nbformat.write(nb, os.path.join(str(testdir.tmpdir), filename))

    # patch the run_server function so that it doesn't actually
    # spawn a server and display the diff.  But the diff is still
    # calculated.
    mocker.patch('nbdime.webapp.nbdiffweb.run_server')
    result = testdir.runpytest_inprocess('--nbval',
                                         '--nbval-current-env',
                                         '--nbdime',
                                         filename)
    # run_server() is only called if there is a discrepancy in the notebook.
    # so it should have been called in this case:
    nbdime.webapp.nbdiffweb.run_server.assert_called_once()

    # note: this import must be AFTER the mocker.patch
    from nbval.nbdime_reporter import EXIT_TESTSFAILED
    assert result.ret == EXIT_TESTSFAILED
