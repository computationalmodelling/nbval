PYTEST ?= py.test
TEST_OPTIONS ?= -v --current-env

all: test

test:
	$(PYTEST) $(TEST_OPTIONS) .
	$(PYTEST) --nbval --current-env --sanitize-with sanitize_defaults.cfg sample_notebook.ipynb
	$(PYTEST) --nbval --current-env latex-example.ipynb

.PHONY: all test
