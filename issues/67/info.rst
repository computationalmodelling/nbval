When running::

  py.test --nbval notebook1.ipynb notebook2.ipynb

the output is::

    ======================================= test session starts ===============
    platform darwin -- Python 3.6.0, pytest-3.0.7, py-1.4.33, pluggy-0.4.0
    rootdir: /Users/fangohr/git/nbval, inifile:
    plugins: nbval-0.6
    collected 2 items

    notebook1.ipynb .
    notebook2.ipynb F

    ============================================ FAILURES =====================
    _____________________________________________ cell 0 ______________________
    Notebook cell execution failed
    Cell 0: Cell outputs differ

    Input:
    import time

    time.time()

    Traceback: mismatch 'text/plain'
    <<<<<<<<<<<< Reference output from ipynb file:
    1498639847.528011
    ============ disagrees with newly computed (test) output:
    1498640219.550588
    >>>>>>>>>>>>
    =============================== 1 failed, 1 passed in 2.07 seconds ========

This is not ideal as we know there is a fail in Cell 0, but  we don't
know in which file. (Here it is ``notebook1.ipynb``).

Suggest that the name of the file in which the reported failures take
place is displayed somehow.
