from setuptools import setup

readme = open('README.rst').read()

setup(
    name="nbval",
    version="0.5",
    author="Laslett, Cortes, Kluyver, Pepper, Fangohr",
    author_email="cmg@soton.ac.uk",
    description='A py.test plugin to validate Jupyter notebooks',
    long_description=readme,
    packages = ['nbval'],
    url='https://github.com/computationalmodelling/nbval',
    # the following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'nbval = nbval.plugin',
        ]
    },
    install_requires = [
        'pytest >= 2.8',
        'six',
        'jupyter_client',
        'nbformat',
        'ipykernel'
    ],
    classifiers = [
        'Framework :: IPython',
        'Framework :: Pytest',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
    ]
)
