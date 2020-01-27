
import coverage

if coverage.version_info >= (5, 0, 0):
    from ._cover5 import setup_coverage, teardown_coverage
else:
    from ._cover4 import setup_coverage, teardown_coverage
