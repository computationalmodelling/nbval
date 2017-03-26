"""
Code to enable coverage of any external code called by the
notebook.
"""

_python_setup = """\
import coverage

__cov = coverage.Coverage(source=%r, config_file=%r, data_suffix='nbval')
__cov.start()
"""
_python_teardown = """\
__cov.stop()
__cov.save()
"""


def setup_coverage(config, kernel, floc, output_loc=None):
    """Start coverage reporting on kernel

    Currently supported kernel languages are:
     - Python
    """
    language = kernel.language
    if language.startswith('python'):
        # Get options from pytest's own coverage module
        source = config.option.cov_source
        config_file = config.option.cov_config
        cmd = _python_setup % (source, config_file)
        msg_id = kernel.kc.execute(cmd, stop_on_error=False)
        kernel.await_idle(msg_id, 60)  # A minute should be plenty to enable coverage
    else:
        config.warn('C1',
            'Coverage currently not supported for language "%s".' % language,
            floc)
        return


def teardown_coverage(config, kernel, output_loc=None):
    language = kernel.language
    if language.startswith('python'):
        msg_id = kernel.kc.execute(_python_teardown)
        kernel.await_idle(msg_id, 60)  # A minute should be plenty to write out coverage
    else:
        # Warnings should be given on setup, or there might be no teardown
        # for a specific language, so do nothing here
        pass
