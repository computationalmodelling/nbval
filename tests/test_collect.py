
from __future__ import print_function

import os

import nbformat


pytest_plugins = "pytester"


def _build_nb(sources):
    """Builds a notebook of only code cells, from a list of sources"""
    nb = nbformat.v4.new_notebook()
    for src in sources:
        nb.cells.append(nbformat.v4.new_code_cell(src))
    return nb


def _write_nb(sources, path):
    nb = _build_nb(sources)
    nbformat.write(nb, path)


# Sources to try to collect
sources = [
    # In [1]:
    "a = 5",
    # In [2]:
    "for i in range(10):\n" +
    "    print(i)",
    # In [3]:
    "print(a)",
    # In [4]:
    "a",
    # In [5]:
    "import os\n" +
    "os.curdir"
]


def test_collection_nbval(testdir):
    # Write notebook to test dir
    _write_nb(sources, os.path.join(str(testdir.tmpdir), 'test_collection.ipynb'))

    # Run tests
    items, recorder = testdir.inline_genitems('--nbval', '--nbval-current-env')

    # Debug output:
    for item in items:
        print('Cell %d:' % item.cell_num)
        print("    " + "\n    ".join(item.cell.source.splitlines()) + "\n")

    # Checks:
    assert len(items) == 5


def test_collection_nbval_lax(testdir):
    # Write notebook to test dir
    _write_nb(sources, os.path.join(str(testdir.tmpdir), 'test_collection.ipynb'))

    # Run tests
    items, recorder = testdir.inline_genitems('--nbval-lax', '--nbval-current-env')

    # Debug output:
    for item in items:
        print('Cell %d:' % item.cell_num)
        print("    " + "\n    ".join(item.cell.source.splitlines()) + "\n")

    # Checks:
    assert len(items) == 5
