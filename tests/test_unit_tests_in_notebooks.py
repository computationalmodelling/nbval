import subprocess

command_template = "py.test --nbval -v "


def runtest(command):
    pass


def test_latex_fail_randomoutput():

    testname = "test-latex-fail-randomoutput"
    command = command_template + testname + ".ipynb"

    correct_outcome = testname.split('-')[2]
    assert correct_outcome in ['pass', 'fail']

    exitcode = subprocess.call(command, shell=True)
    if correct_outcome is 'pass':
        assert exitcode is 0
    elif correct_outcome is 'fail':
        assert exitcode is not 0

    # test-latex-fail-randomoutput.ipynb
    # test-latex-pass-correctouput.ipynb
    # test-latex-pass-failsbutignoreoutput.ipynb


def test_latex_pass_correctoutput():

    testname = "test-latex-pass-correctouput"
    command = command_template + testname + ".ipynb"

    correct_outcome = testname.split('-')[2]
    assert correct_outcome in ['pass', 'fail']

    exitcode = subprocess.call(command, shell=True)
    if correct_outcome is 'pass':
        assert exitcode is 0
    elif correct_outcome is 'fail':
        assert exitcode is not 0


def test_latex_pass_failsbutignoreoutput():

    testname = "test-latex-pass-failsbutignoreoutput"
    command = command_template + testname + ".ipynb"

    correct_outcome = testname.split('-')[2]
    assert correct_outcome in ['pass', 'fail']

    exitcode = subprocess.call(command, shell=True)
    if correct_outcome is 'pass':
        assert exitcode is 0
    elif correct_outcome is 'fail':
        assert exitcode is not 0


    # test-latex-pass-correctouput.ipynb
    # test-latex-pass-failsbutignoreoutput.ipynb
