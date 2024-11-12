from setuptools import setup

from nbval._version import __version__

with open('README.md') as f:
    readme = f.read()

setup(
    name="nbval",
    version=__version__,
    author="Laslett, Cortes, Fauske, Kluyver, Pepper, Fangohr",
    description='A py.test plugin to validate Jupyter notebooks',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages = ['nbval'],
    url='https://github.com/computationalmodelling/nbval',
    # the following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'nbval = nbval.plugin',
        ]
    },
    install_requires = [
        'pytest >= 7',
        'jupyter_client',
        'nbformat',
        'ipykernel',
        'coverage',
    ],
    python_requires='>=3.8, <4',
    classifiers = [
        'Framework :: IPython',
        'Framework :: Pytest',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
    ]
)
