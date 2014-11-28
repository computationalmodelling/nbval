from setuptools import setup

setup(
    name="stollen",
    packages = ['stollen'],

    # the following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'name_of_plugin = stollen.plugin',
        ]
    },
)
