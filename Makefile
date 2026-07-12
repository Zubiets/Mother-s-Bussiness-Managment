.PHONY: init venv test

init:	
	pip install -r requirements.txt

venv:
	python -m venv venv
	. venv/bin/activate

test:
	python -m pytest

run:
	TCL_LIBRARY_PATH=/usr/share/tcltk/tcl8.6 TK_LIBRARY_PATH=/usr/share/tcltk/tk8.6 ./venv/bin/python main.py