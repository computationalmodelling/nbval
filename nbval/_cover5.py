"""
Code to enable coverage of any external code called by the
notebook.

For coverage.py >= v 5.0.0
"""

import os
import coverage
import warnings


# Coverage setup/teardown code to run in kernel
# Inspired by pytest-cov code.
_python_setup = """\
import coverage

__cov = coverage.Coverage(
    data_file=%r,
    source=%r,
    config_file=%r,
    auto_data=True,
    data_suffix='.nbval',
    )
__cov.load()
__cov.start()
__cov._warn_no_data = False
__cov._warn_unimported_source = False
"""
_python_teardown = """\
__cov.stop()
__cov.save()
"""


def setup_coverage(config, kernel, floc, output_loc=None):
    """Start coverage reporting in kernel.

    Currently supported kernel languages are:
     - Python
    """

    language = kernel.language
    if language.startswith('python'):
        # Get the pytest-cov coverage object
        cov = get_cov(config)
        if cov:
            # If present, copy the data file location used by pytest-cov
            data_file = os.path.abspath(cov.get_data().data_filename())
        else:
            # Fall back on output_loc and current dir if not
            data_file = os.path.abspath(os.path.join(output_loc or os.getcwd(), '.coverage'))

        # Get options from pytest-cov's command line arguments:
        source = config.option.cov_source
        config_file = config.option.cov_config
        if isinstance(config_file, str) and os.path.isfile(config_file):
            config_file = os.path.abspath(config_file)

        # Build setup command and execute in kernel:
        cmd = _python_setup % (data_file, source, config_file)
        msg_id = kernel.kc.execute(cmd, stop_on_error=False)
        kernel.await_idle(msg_id, 60)  # A minute should be plenty to enable coverage
    else:
        warnings.warn_explicit(
            'Coverage currently not supported for language %r.' % language,
            category=UserWarning,
            filename=floc[0] if floc else '',
            lineno=0
        )
        return


def teardown_coverage(config, kernel, output_loc=None):
    """Finish coverage reporting in kernel.

    The coverage should previously have been started with
    setup_coverage.
    """
    language = kernel.language
    if language.startswith('python'):
        # Teardown code does not require any input, simply execute:
        msg_id = kernel.kc.execute(_python_teardown)
        kernel.await_idle(msg_id, 60)  # A minute should be plenty to write out coverage

    else:
        # Warnings should be given on setup, or there might be no teardown
        # for a specific language, so do nothing here
        pass


def get_cov(config):
    """Returns the coverage object of pytest-cov."""

    # Check with hasplugin to avoid getplugin exception in older pytest.
    if config.pluginmanager.hasplugin('_cov'):
        plugin = config.pluginmanager.getplugin('_cov')
        if plugin.cov_controller:
            return plugin.cov_controller.cov
    return None
