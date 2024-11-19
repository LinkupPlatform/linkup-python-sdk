install:
	@echo "Installing local package..."
	pip install .
install-dev:
	@echo "Installing local package in developper mode..."
	pip install -e .
	pip install -r requirements-dev.txt
