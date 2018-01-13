from setuptools import setup

setup(
    name="nbval",
    version="0.7",
    author="Laslett, Cortes, Kluyver, Pepper, Fangohr",
    description='A py.test plugin to validate Jupyter notebooks',
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
    extras_require = {
        'test': ['matplotlib', 'sympy'],
    },
    classifiers = [
        'Framework :: IPython',
        'Framework :: Pytest',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
    ]
)
