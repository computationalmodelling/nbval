
import nbformat


def build_nb(sources):
    """Builds a notebook of only code cells, from a list of sources
    """
    nb = nbformat.v4.new_notebook()
    for src in sources:
        nb.cells.append(nbformat.v4.new_code_cell(src))
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
