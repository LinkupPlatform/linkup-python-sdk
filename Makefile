install:
	@echo "Installing local package..."
	uv sync
	uv run pre-commit install
install-dev:
	@echo "Installing local package in developper mode..."
	uv pip install -e ".[dev]"
	uv run pre-commit install
test:
	@echo "Running tests..."
	pre-commit run --all-files
	mypy .
	# Follow the test practices recommanded by LangChain (v0.3)
	# See https://python.langchain.com/docs/contributing/how_to/integrations/standard_tests/
	pytest --cov=linkup/ --cov-report term-missing --disable-socket --allow-unix-socket tests/unit_tests
	# TODO: uncomment the following line when integration tests are ready
	# pytest tests/integration_tests
