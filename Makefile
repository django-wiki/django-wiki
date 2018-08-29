.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:  ## Check python code conventions
	flake8 src/wiki tests/

test:  ## Run automated test suite
	pytest

test-all:  ## Run tests on all supported Python environments
	tox

coverage:  ## Generate test coverage report
	coverage run --source wiki setup.py test
	coverage report -m

translation-push:  ## Updates and pushes
	cd src/wiki && django-admin makemessages -l en
	cd ..
	tx push -s

translation-pull:  ## Pulls translation languages
	tx pull -a
	cd src/wiki && django-admin compilemessages

docs: ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	rm -f docs/wiki*.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/wiki
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

docs-linkcheck:
	sphinx-build -b linkcheck ./docs ./docs/_build


release: dist  ## Generate and upload release to PyPi
	@echo ""
	@echo "Release check list:"
	@echo ""
	@echo "1. Release notes?"
	@echo "2. Pushed source language to transifex?"
	@echo "3. Pulled new translations from transifex?"
	@echo "4. Built and committed new assets?"
	@echo "5. Did you do a signed commit and push to Github?"
	@echo "6. Check that the .whl and .tar.gz dists work - e.g. that MANIFEST.in is updated."
	@echo ""
	@read -p "CTRL+C or ENTER" dummy
	twine upload -s dist/*

assets:  ## Build CSS files
	lessc src/wiki/static/wiki/bootstrap/less/wiki/wiki-bootstrap.less src/wiki/static/wiki/bootstrap/css/wiki-bootstrap.css
	lessc -x src/wiki/static/wiki/bootstrap/less/wiki/wiki-bootstrap.less src/wiki/static/wiki/bootstrap/css/wiki-bootstrap.min.css

dist: clean assets  ## Generate wheels distribution
	python setup.py bdist_wheel
	python setup.py sdist
	ls -l dist
