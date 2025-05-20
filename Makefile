.PHONY: clean test lint coverage build install dev-install

# Default target
all: clean lint test

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

# Run tests
test:
	pytest

# Run tests with coverage
coverage:
	pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "HTML coverage report generated in htmlcov/"

# Run linting
lint:
	flake8 src tests

# Build package
build: clean
	python -m build

# Install package
install: build
	pip install dist/*.whl

# Install package in development mode
dev-install:
	pip install -e .

# Run the web application
run-web:
	streamlit run src/app.py

# Run the CLI application
run-cli:
	python -m src.cli