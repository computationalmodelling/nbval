import os

import nbformat

import pytest

from utils import build_nb


pytest_plugins = "pytester"

@pytest.mark.parametrize("magic, expected_pass", [
    (r"%dirs", True),
    (r"%precision bad", False),
    (r"%this_magic_does_not_exist", False)
])
def test_magics(testdir, magic, expected_pass):
    nb = build_nb([
        # In [1]:
        magic,
    ])
    nb_name = 'test_magics'
    nbformat.write(nb, os.path.join(
        str(testdir.tmpdir), nb_name+".ipynb"))

    # using subprocess because otherwise second and subsequent tests always fail (some state left over somewhere in the jupyter stack)
    result = testdir.runpytest_subprocess('--nbval-lax', '--current-env', '-s', '-v')

    assert result.ret == (not expected_pass)

    result.stdout.fnmatch_lines_random(
        ["*collected 1 item*",
         "{nb_name}::ipynb::Cell 0 {result}".format(nb_name=nb_name, result="PASSED" if expected_pass else "FAILED")])
