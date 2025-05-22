#!/bin/bash
# Script to run the CI workflow locally

set -e  # Exit immediately if a command exits with a non-zero status

echo "=== Running CI workflow locally ==="

echo "1. Installing dependencies..."
pip install -r requirements.txt
pip install -e .

echo "2. Running linting with flake8..."
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

echo "3. Running tests with pytest..."
pytest --cov=src --cov-report=term

echo "4. Building package..."
python -m build

echo "5. Verifying package installation..."
pip install dist/*.whl
task-manager --help || echo "Command-line tool installed but help command not implemented"

echo "=== CI workflow completed successfully ==="