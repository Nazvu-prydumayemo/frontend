.PHONY: run lint format fix type test build run-web run-web-tunnel help

ifeq ($(OS),Windows_NT)
    PYTHON := py
else
    PYTHON := $(shell which python3 2>/dev/null || which python 2>/dev/null)
endif

run:
	python -m tuiapp.main

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

run-web:
	python -m tuiapp.serve

run-web-tunnel:
	PUBLIC_URL=$(PUBLIC_URL) python -m tuiapp.serve

help:
	@echo "Available targets:"
	@echo "  make run     - Run the TUI app"
	@echo "  make lint    - Run ruff checks"
	@echo "  make format  - Format code with ruff"
	@echo "  make fix     - Auto-fix lint issues"
	@echo "  make type    - Run mypy"
	@echo "  make test    - Run pytest"
	@echo "  make build   - Build executable with PyInstaller"
	@echo "  make run-web - Run TUI app in browser via textual-serve (port 8080)"
	@echo "  make run-web-tunnel - Run via textual-serve with PUBLIC_URL (Cloudflare Tunnel)"
	@echo ""
	@echo "Python: $(PYTHON)"