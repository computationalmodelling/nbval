import sys
sys.path.append('..')
import textwrap
from pytest_validate_nb.plugin import *


def test_read_sanitize_patterns():
    file_contents = textwrap.dedent("""
        [Section1]
        regex: foo
        replace: bar1

        regex: quux
        replace: 42

        [Section2 (overwrites regex 'foo')]
        regex: foo
        replace: bar2
        """)

    patterns = read_sanitize_patterns(file_contents)
    assert patterns == {'foo': 'bar2',
                       'quux': '42',
                       }
