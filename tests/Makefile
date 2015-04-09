PYTEST ?= py.test
TEST_OPTIONS ?= -sv

all: test

test:
	$(PYTEST) $(TEST_OPTIONS) .
	$(PYTEST) --ipynb --sanitize-with sanitize_defaults.cfg sample_notebook.ipynb

.PHONY: all test
