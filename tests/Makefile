PYTEST ?= py.test
TEST_OPTIONS ?= -sv

all: test

test:
	$(PYTEST) $(TEST_OPTIONS) .
	$(PYTEST) --nbval --current-env --sanitize-with sanitize_defaults.cfg sample_notebook.ipynb

.PHONY: all test
