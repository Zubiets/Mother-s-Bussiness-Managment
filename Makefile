.PHONY: init venv test

init:	
	pip install -r requirements.txt

venv:
	python3 -m venv venv
	. venv/bin/activate

test:
	python -m pytest

run:
	python -m main