install:
	uv sync
install-dev:
	@$(MAKE) install
	uv run pre-commit install

format-lint:
	SKIP=no-commit-to-branch uv run pre-commit run --all-files
format-lint-unsafe:
	uv run --with ruff ruff check --fix --unsafe-fixes .
	@echo
	@$(MAKE) format-lint

test-mypy:
	@# Avoid running mypy on the whole directory ("./") to avoid potential conflicts with files with the same name (e.g. between different types of tests)
	uv run mypy ./src/
	uv run mypy ./tests/unit/
test-pytest:
	uv run pytest --cov=src/linkup/ ./tests/unit/
test:
	@$(MAKE) test-mypy
	@echo
	@$(MAKE) test-pytest

update-uv:
	uv lock --upgrade
	uv sync
update-pre-commit:
	uv run pre-commit autoupdate

clean:
	rm -rf dist/
	rm -f .coverage
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf **/*/__pycache__/
