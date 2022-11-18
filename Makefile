define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"



docs: ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	rm -f docs/wiki*.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/wiki
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html


