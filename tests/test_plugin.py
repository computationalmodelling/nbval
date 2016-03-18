import sys
sys.path.append('..')
import textwrap
from nbval.plugin import *


def test_get_sanitize_patterns():
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

    patterns = get_sanitize_patterns(file_contents)
    assert patterns == [('foo', 'bar1'),
                        ('quux', '42'),
                        ('foo', 'bar2'),
                       ]
