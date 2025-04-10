.PHONY: lint format test
RUFF := .venv/bin/ruff
PYTEST := .venv/bin/pytest

lint:
	$(RUFF) check

format:
	$(RUFF) check --fix
	$(RUFF) format .

test:
	$(PYTEST) --cov=. --cov-report=term
