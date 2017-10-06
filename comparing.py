import numpy
import pandas

def arraylike_equal(test,ref):
    # based on np assert array equal (so e.g. nan==nan)
    try:
        numpy.testing.assert_array_equal(test,ref)
        return True
    except AssertionError:
        return False

handlers = {}
handlers[pandas.DataFrame] = arraylike_equal
handlers[numpy.ndarray] = arraylike_equal

import inspect
def get_handler(class_):
    for class_ in inspect.getmro(class_)[::-1]:
        if class_ in handlers:
            return handlers[class_]
    return lambda test,ref: test==ref

# TODO: would be nice to get useful info about differences, e.g. numpy
# testing's array comparison output
