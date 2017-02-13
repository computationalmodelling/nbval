PYTHON ?= python3

test:
	@# Note: to run the tests, we also need additional dependencies
	@# ("make install-test-deps")
	py.test -v tests/ --nbval --current-env --sanitize-with tests/sanitize_defaults.cfg --ignore tests/ipynb-test-samples

build-dists:
	rm -rf dist/
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel

release: build-dists
	twine upload dist/*


install-test-deps:
	pip install matplotlib sympy
