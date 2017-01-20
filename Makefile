PYTHON ?= python3

test:
	py.test tests/ --nbval --current-env --sanitize-with tests/sanitize_defaults.cfg --ignore tests/ipynb-test-samples

build-dists:
	rm -rf dist/
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel

release: build-dists
	twine upload dist/*
