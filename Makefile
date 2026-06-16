.PHONY: init venv test

init:	
	pip install -r requirements.txt

venv:	
	. venv/bin/activate

test:
	python -m pytest