install:
	uv sync
install-dev:
	@$(MAKE) install
	uv run pre-commit install

test:
	@echo "Running tests..."
	uv run pre-commit run --all-files
	uv run mypy .
	# Follow the test practices recommanded by LangChain (v0.3)
	# See https://python.langchain.com/docs/contributing/how_to/integrations/standard_tests/
	uv run pytest --cov=src/linkup/ --cov-report term-missing --disable-socket --allow-unix-socket tests/unit_tests
	# TODO: uncomment the following line when integration tests are ready
	# pytest tests/integration_tests
