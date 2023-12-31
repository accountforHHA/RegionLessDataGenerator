VENV=.venv
PYTHON=/usr/bin/python3.8

venv:
	${PYTHON} -m venv ${VENV}


dir:
	mkdir log