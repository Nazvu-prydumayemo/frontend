.PHONY: run lint format fix type test build help

ifeq ($(OS),Windows_NT)
    PYTHON := py
else
    PYTHON := $(shell which python3 2>/dev/null || which python 2>/dev/null)
endif

run:
	$(PYTHON) -m tuiapp.main

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

build:
	$(PYTHON) build.py

help:
	@echo "Available targets:"
	@echo "  make run     - Run the TUI app"
	@echo "  make lint    - Run ruff checks"
	@echo "  make format  - Format code with ruff"
	@echo "  make fix     - Auto-fix lint issues"
	@echo "  make type    - Run mypy"
	@echo "  make test    - Run pytest"
	@echo "  make build   - Build executable with PyInstaller"
	@echo ""
	@echo "Python: $(PYTHON)"