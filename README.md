# Py.test plugin for IPython notebook validation

The plugin adds functionality to py.test to recognise and collect IPython
notebooks. The intended purpose of the tests is to determine whether execution
of the stored inputs match the stored outputs of the `.ipynb` file.

The tests were designed to ensure that IPython notebooks (especially those for
reference and documentation), are executing consistently.

Each cell is taken as a test, a cell that doesn't reproduce the expected
output will fail.

See `documentation.ipynb` for the full documentation.

## Installation
After cloning this repository, the plugin is installed doing

    sudo pip install .

from the main directory. It can be easily removed with:

    sudo pip uninstall pytest_validate_nb


## How it works
The extension looks through every cell that contains code in an IPython notebook
and then the `py.test` system compares the outputs stored in the notebook
with the outputs of the cells when they are executed. Thus, the notebook itself is
used as a testing function.
The output lines when executing the notebook can be sanitized passing an
extra option and file, when calling the `py.test` command. This file
is a usual configuration file for the `ConfigParser` library.

Regarding the execution, roughly, the script initiates an
IPython Kernel with a `shell` and
an `iopub` sockets. The `shell` is needed to execute the cells in
the notebook (it sends requests to the Kernel) and the `iopub` provides 
an interface to get the messages from the outputs. The contents
of the messages obtained from the Kernel are organised in dictionaries
with different information, such as time stamps of executions,
cell data types, cell types, the status of the Kernel, username, etc.

In general, the functionality of the IPython notebook system is 
quite complex, but a detailed explanation of the messages
and how the system works, can be found here 

http://ipython.org/ipython-doc/stable/development/messaging.html

## Execution
To execute this plugin, you need to execute `py.test` with the `ipynb` flag
to differentiate the testing from the usual python files:

    py.test --ipynb

This will execute all the `.ipynb` files in the current folder. Alternatively,
it can be executed:

    py.test --ipynb my_notebook.ipynb

for an specific notebook. 
If the output lines are going to be sanitized, an extra flag, `--sanitize-with`
together with the path to a confguration file with regex expressions, must be passed,
i.e.

    py.test --ipynb my_notebook.ipynb --sanitize-with path/to/my_sanitize_file

where `my_sanitize_file` has the following structure.

```
[Section1]
regex: [a-z]* 
replace: abcd

regex: [1-9]*
replace: 0000

[Section2]
regex: foo
replace: bar
```

The `regex` option contains the expression that is going to be matched in the outputs, and
`replace` is the string that will replace the `regex` match. Currently, the section
names do not have any meaning or influence in the testing system, it will take
all the sections and replace the corresponding options.

## Help
The `py.test` system help can be obtained with `py.test -h`, which will
show all the flags that can be passed to the command, such as the
verbose `-v` option. The IPython notebook plugin can be found under the
`general` section.


## Ackowledgements
This plugin was inspired by Andrea Zonca's py.test plugin for collecting unit
tests in the IPython notebooks ( https://github.com/zonca/pytest-ipynb ).


It is mostly based on the template in https://gist.github.com/timo/2621679 
and the code of a testing system for notebooks https://gist.github.com/minrk/2620735
which we integrated and mixed with the `py.test` system.

## Authors

David Cortes-Ortuno, Oliver Laslett, Maximilian Albert, Ondrej Hovorka, Hans Fangohr

University of Southampton, 2014 - 2015, http://www.southampton.ac.uk
