# CI/CD Workflow Documentation

This document explains the Continuous Integration and Continuous Deployment (CI/CD) workflow set up for the Task Manager project.

## Overview

The Task Manager project uses GitHub Actions to automate testing and ensure code quality. The workflow is designed to run automatically on:

1. Every pull request to any branch
2. Every push to the main branch
3. On a daily schedule (to catch issues with dependency updates)

## Workflow Components

### 1. Pull Request Testing (`python-app.yml`)

This workflow runs on every pull request and push to the main branch:

- **Trigger**: Pull requests to any branch, pushes to main
- **Python Versions**: Tests on Python 3.8, 3.9, 3.10, and 3.11
- **Steps**:
  - Checkout code
  - Set up Python environment
  - Cache dependencies
  - Install dependencies
  - Lint code with flake8
  - Run tests with pytest
  - Generate and upload test coverage report

### 2. Scheduled Testing (`scheduled-tests.yml`)

This workflow runs on a daily schedule:

- **Trigger**: Daily at midnight UTC, or manual trigger
- **Python Version**: 3.10
- **Steps**: Same as the PR testing workflow

## Test Coverage

The workflows generate test coverage reports using pytest-cov and upload them to Codecov. This helps maintain and improve code quality by:

- Tracking which parts of the code are covered by tests
- Identifying areas that need more testing
- Preventing regressions in test coverage

## Badge

The README includes a status badge that shows the current status of the tests on the main branch:

```markdown
[![Test PR](https://github.com/yourusername/task-manager/actions/workflows/python-app.yml/badge.svg)](https://github.com/yourusername/task-manager/actions/workflows/python-app.yml)
```

## Local Testing

Before submitting a PR, contributors should run tests locally:

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest

# Check test coverage
pytest --cov=src
```

## Troubleshooting Failed Tests

If the CI workflow fails:

1. Click on the failed workflow run in the GitHub Actions tab
2. Examine the logs for the specific step that failed
3. Fix the issues in your local repository
4. Push the changes to update the PR

## Adding New Tests

When adding new features or fixing bugs:

1. Add appropriate tests in the `tests/` directory
2. Ensure the tests cover both normal operation and edge cases
3. Run the tests locally before submitting a PR
4. Check that test coverage is maintained or improved