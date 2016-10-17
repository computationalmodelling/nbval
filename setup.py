from setuptools import setup

setup(
    name="nbval",
    version="0.3.5",
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
    classifiers = [
        'Framework :: IPython',
        'Framework :: Pytest',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
    ]
)
