from setuptools import setup

setup(
    name="pytest_validate_nb",
    packages = ['pytest_validate_nb'],

    # the following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'name_of_plugin = pytest_validate_nb.plugin',
        ]
    },
)
