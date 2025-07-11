#!/bin/bash
#
# Script to run tests with coverage

# Run tests with coverage
pytest --cov=src --cov-report=term --cov-report=html

# Open coverage report if on a desktop environment
if [ -n "$DISPLAY" ]; then
    xdg-open htmlcov/index.html 2>/dev/null || open htmlcov/index.html 2>/dev/null || echo "Coverage report generated at htmlcov/index.html"
else
    echo "Coverage report generated at htmlcov/index.html"
fi