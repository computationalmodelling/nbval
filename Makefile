test:
	py.test tests/ --nbval --current-env --sanitize-with tests/sanitize_defaults.cfg --ignore tests/ipynb-test-samples
