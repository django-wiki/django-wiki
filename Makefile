upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade:
	pip install -q -r requirements/pip_tools.txt
	pip-compile --upgrade -o requirements/pip_tools.txt requirements/pip_tools.in
	pip-compile --upgrade -o requirements/base.txt requirements/base.in
	pip-compile --upgrade -o requirements/docs.txt requirements/docs.in
