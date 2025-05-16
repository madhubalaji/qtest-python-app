# Contributing to Task Manager

Thank you for your interest in contributing to Task Manager! This document provides guidelines and instructions for contributing to this project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment:
   ```
   pip install -r requirements.txt
   pip install -e .
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with descriptive commit messages:
   ```
   git commit -m "Add feature: your feature description"
   ```

3. Run tests locally to ensure your changes don't break existing functionality:
   ```
   pytest
   ```

4. Push your branch to your fork:
   ```
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request (PR) from your fork to the main repository

## Pull Request Process

When you submit a pull request, our automated testing workflow will run:

1. The workflow will test your code on multiple Python versions (3.8, 3.9, 3.10, 3.11)
2. It will check code style with flake8
3. It will run all tests and generate a coverage report

You can see the status of these checks directly in your PR. If any checks fail, please fix the issues and push the changes to your branch - the tests will run again automatically.

### PR Requirements

For your PR to be accepted:

- All automated tests must pass
- New code should be covered by tests
- Code should follow the project's style guidelines
- Documentation should be updated if necessary

## Code Style

This project follows PEP 8 style guidelines. You can check your code with flake8:

```
flake8 .
```

## Testing

Write tests for new features and bug fixes. Run the test suite with:

```
pytest
```

To see test coverage:

```
pytest --cov=src
```

## Questions?

If you have any questions about contributing, please open an issue in the repository.

Thank you for contributing to Task Manager!