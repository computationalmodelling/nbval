
import nbformat


def build_nb(sources, mark_run=False):
    """Builds a notebook of only code cells, from a list of sources
    """
    nb = nbformat.v4.new_notebook()
    execution_count = 1
    for src in sources:
        cell = nbformat.v4.new_code_cell(src)
        if mark_run:
            cell.execution_count = execution_count
            execution_count += 1
        nb.cells.append(cell)
    return nb


def add_expected_plaintext_outputs(nb, outputs):
    for i, (cell, text) in enumerate(zip(nb.cells, outputs)):
        if text is None:
            continue
        output = nbformat.v4.new_output(
            'execute_result',
            data={'text/plain': [text]},
            execution_count=i,
            )
        cell.outputs.append(output)
