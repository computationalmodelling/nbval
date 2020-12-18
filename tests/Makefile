PYTEST ?= py.test
TEST_OPTIONS ?= -v --nbval-current-env

all: test

test:
	$(PYTEST) $(TEST_OPTIONS) .
	$(PYTEST) --nbval --nbval-current-env --nbval-sanitize-with sanitize_defaults.cfg sample_notebook.ipynb
	$(PYTEST) --nbval --nbval-current-env latex-example.ipynb

.PHONY: all test
