install:
	uv sync
install-dev:
	@$(MAKE) install
	uv run prek install

lint:
	SKIP=no-commit-to-branch uv run prek run --all-files

typecheck:
	@# Ignore pyright-python warnings (only warn when a new pyright version is available)
	PYRIGHT_PYTHON_IGNORE_WARNINGS=1 uv run pyright

test:
	uv run pytest --cov=src/linkup/ ./tests/unit/

update-dependencies:
	uv lock --upgrade
update-pre-commit-hooks:
	uv run prek autoupdate --cooldown-days 14

clean:
	rm -rf dist/
	rm -f .coverage
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf **/*/__pycache__/
