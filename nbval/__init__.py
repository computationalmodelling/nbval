"""
A pytest plugin for testing and validating ipython notebooks
"""

__version__ = '0.3.6'


# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `nbval` directory
        src="celltoolbar",
        # directory in the `nbextension/` namespace
        dest="nbval",
        # _also_ in the `nbextension/` namespace
        require="nbval/index")]
