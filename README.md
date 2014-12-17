# Py.test plugin for iPython notebooks

This code idea is a modification of the plugin that extends the functionality 
of the `py.test` testing system for ipython notebooks 
( https://github.com/zonca/pytest-ipynb ).

It is mostly based on the template in https://gist.github.com/timo/2621679 
and the code of a testing system for notebooks https://gist.github.com/minrk/2620735
which we integrated and mixed with the `py.test` system.

Additionally, we added an option to create a configuration file with
`regex`s which are used to sanitize strings in the outputs of the
iPython reference notebook, when executed. 

## How it works
The extension looks through every cell that contains code in an ipython notebook
an then the `py.test` system compares the outputs of the notebook
(before being processed) with the 
outputs of the cells when they are executed. Thus, the notebook itself is
used as a testing function.
The output lines when executing the notebook can be sanitized passing an
extra option and file, when calling the `py.test` command. This file
is a usual configuration file for the `ConfigParser` library.

Regarding the execution, roughly, the script initiates an
iPython Kernel with a `shell` and
an `iopub` sockets. The `shell` is needed to execute the cells in
the notebook (it sends requests to the Kernel) and the `iopub` provides 
an interface to get the messages from the outputs. The contents
of the messages obtained from the Kernel are organised in dictionaries
with different information, such as time stamps of executions,
cell data types, cell types, the status of the Kernel, username, etc.

In general, the functionality of the ipython notebook system is 
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
If the output lines are going to be sanitized, an extra flag, `--sanitize_file`
together with the path to a confguration file with regex expressions, must be passed,
i.e.

    py.test --ipynb my_notebook.ipynb --sanitize_file path/to/my_sanitize_file

where `my_sanitize_file` has the structure

```
[regex1]
regex: [a-z]* 
replace: abcd

[regex2]
regex: [1-9]*
replace: 0000
```

The `regex` option contains the expression that is going to be matched in the outputs, and
`replace` is the string that will replace the `regex` match. Currently, the section
names do not have any meaning or influence in the testing system, it will take
all the sections and replace the corresponding options.

Examples of a notebook and regex file are found in the `finmag_nb_test.ipynb`
and `regex_sanitize` files, correspondingly.

## Installation
For now, the project is called `stollen`. After cloning this repository, the
plugin is installed doing

    sudo pip install .

from the main directory. It can be easily removed with:

    sudo pip uninstall stollen

## Tests
The `py.test` system provides the base system, for the outputs in the console.
For example

    py.test --ipynb finmag_nb_test.ipynb --sanitize_file regex_sanitize

will produce

```

=================================== test session starts ====================================
platform linux2 -- Python 2.7.6 -- py-1.4.20 -- pytest-2.5.2
plugins: stollen
collected 8 items 

finmag_nb_test.ipynb .FF..FF.

========================================= FAILURES =========================================
__________________________________________ cell 2 __________________________________________
Notebook execution failed
Cell 2: Error with cell

Input:
sim = finmag.example.barmini()

Traceback:
Mismatch number of outputs in cell

__________________________________________ cell 3 __________________________________________
Notebook execution failed
Cell 3: Error with cell

Input:
sim.run_until(1e-10)

Traceback:
Mismatch number of outputs in cell

__________________________________________ cell 7 __________________________________________
Notebook execution failed
Cell 7: Error with cell

Input:
print [np.random.rand() for i in range(4)]
print [np.random.rand() for i in range(4)]

Traceback:
mismatch text:
[0.8138240863751218, 0.5542320678041717, 0.4118839647182173, 0.43531249806206707]
[0.9825349878065949, 0.6601684143399118, 0.6098945000301015, 0.010376910854703048]

  !=  
[0.8827183866873831, 0.6374475831607065, 0.9714307435688422, 0.5429659593925313]
[0.4135221535721476, 0.5592454549210213, 0.7262998989524039, 0.5689598602201745]


__________________________________________ cell 8 __________________________________________
Notebook execution failed
Cell 8: Error with cell

Input:
# This is meant to fail when the number of lines
# mismatch
for i in range(np.random.randint(1, 8)):
    print 1

Traceback:
mismatch text:
1
1

  !=  
1
1
1
1
1
1


=========================== 4 failed, 4 passed in 14.94 seconds ============================
```

Currently, image files are not compared, but from the original script,
it can be implemented a function to take this into account
in the future.

Furthermore, when the number of output lines from the executed outputs
differ from the total of lines from the reference, the traceback
will show a `Mismatch number of outputs in cell` message.

## Help
The `py.test` system help can be obtained with `py.test -h`, which will
show all the flags that can be passed to the command, such as the
verbose `-v` option. The ipython notebook plugin can be found under the
`general` section.
