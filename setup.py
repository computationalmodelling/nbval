from setuptools import setup

setup(
    name="nbval",
    version="0.2",
    author="Laslett, Cortes, Kluyver, Fangohr",
    packages = ['nbval'],

    # the following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'name_of_plugin = nbval.plugin',
        ]
    },
)
