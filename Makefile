VENV_BIN=venv/bin

venv:
	python3 -m venv venv

install: venv
	$(VENV_BIN)/pip install .

run: install
	$(VENV_BIN)/python app.py -h

clean:
	rm -rf venv .out .pytest_cache .tox  dist build
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete