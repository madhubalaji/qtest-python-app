.PHONY: help install test test-cov lint format clean build

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=src --cov-report=term-missing --cov-report=html

lint:  ## Run linting
	flake8 .

format:  ## Format code with black
	black .

format-check:  ## Check code formatting
	black --check --diff .

clean:  ## Clean up generated files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python -m build

dev-install:  ## Install in development mode
	pip install -e .

all-checks:  ## Run all checks (lint, format-check, test)
	make lint
	make format-check
	make test-cov

ci:  ## Run CI pipeline locally
	make all-checks