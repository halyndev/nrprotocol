.PHONY: install test lint type-check clean

install:
	pip install -e .

test:
	cd sdk/python && python -m pytest -v

lint:
	ruff check sdk/python/

type-check:
	mypy sdk/python/nrp/ --ignore-missing-imports

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name '*.pyc' -delete
