.PHONY: run lint format fix type test help

run:
	py -m tuiapp.main

lint:
	ruff check .

format:
	ruff format .

fix:
	ruff check . --fix

type:
	mypy src/

test:
	pytest

help:
	@echo "Available targets:"
	@echo "  make run     - Run the TUI app"
	@echo "  make lint    - Run ruff checks"
	@echo "  make format  - Format code with ruff"
	@echo "  make fix     - Auto-fix lint issues"
	@echo "  make type    - Run mypy"
	@echo "  make test    - Run pytest"