install:
	@echo "Installing local package..."
	pip install .
install-dev:
	@echo "Installing local package in developper mode..."
	pip install -e .
	pip install -r requirements-dev.txt
	pre-commit install
test:
	@echo "Running tests..."
	pre-commit run --all-files
	mypy .
	# Follow the test practices recommanded by LangChain (v0.3)
	# See https://python.langchain.com/docs/contributing/how_to/integrations/standard_tests/
	pytest --cov=linkup/ --cov-report term-missing tests/unit_tests
	# TODO: uncomment the following line when integration tests are ready
	# pytest tests/integration_tests
