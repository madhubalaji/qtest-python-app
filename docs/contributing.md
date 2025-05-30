# Contributing Guidelines

Thank you for your interest in contributing to the Task Manager project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## How to Contribute

There are many ways to contribute to the Task Manager project:

1. **Reporting Bugs**: If you find a bug, please report it by creating an issue.
2. **Suggesting Enhancements**: If you have ideas for new features or improvements, please suggest them by creating an issue.
3. **Writing Code**: If you want to contribute code, please follow the guidelines below.
4. **Improving Documentation**: If you find errors or gaps in the documentation, please help improve it.
5. **Reviewing Pull Requests**: If you're familiar with the project, you can help review pull requests.

## Reporting Bugs

When reporting bugs, please include:

1. A clear and descriptive title
2. A detailed description of the bug
3. Steps to reproduce the bug
4. Expected behavior
5. Actual behavior
6. Screenshots (if applicable)
7. Environment information (OS, Python version, etc.)

## Suggesting Enhancements

When suggesting enhancements, please include:

1. A clear and descriptive title
2. A detailed description of the enhancement
3. Why the enhancement would be useful
4. Any relevant examples or mockups

## Contributing Code

### Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager
   ```
3. Set up the development environment as described in the [Development Guide](development.md)
4. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. Make your changes to the code
2. Write or update tests for your changes
3. Update documentation to reflect your changes
4. Run the tests to ensure they pass:
   ```bash
   pytest
   ```
5. Format your code:
   ```bash
   black src tests
   isort src tests
   ```
6. Check for linting errors:
   ```bash
   flake8 src tests
   ```

### Submitting Changes

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Add your descriptive commit message here"
   ```
2. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
3. Create a pull request from your fork to the main repository

### Pull Request Guidelines

When submitting a pull request, please:

1. Include a clear and descriptive title
2. Include a detailed description of the changes
3. Reference any related issues
4. Ensure all tests pass
5. Update documentation as needed
6. Follow the code style guidelines

## Code Style Guidelines

Please follow these code style guidelines:

1. **PEP 8**: Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code
2. **Docstrings**: Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for functions, methods, and classes
3. **Type Hints**: Use type hints for function and method signatures
4. **Line Length**: Limit lines to 88 characters (compatible with Black)

## Testing Guidelines

When writing tests, please follow these guidelines:

1. Write tests for all new features and bug fixes
2. Ensure tests are isolated and don't depend on external resources
3. Use descriptive test names that explain what the test is checking
4. Use assertions to verify expected behavior
5. Aim for high test coverage

## Documentation Guidelines

When updating documentation, please follow these guidelines:

1. Use clear and concise language
2. Provide examples where appropriate
3. Keep the documentation up-to-date with the code
4. Check for spelling and grammar errors

## Review Process

All pull requests will be reviewed by the project maintainers. The review process includes:

1. Checking that the code follows the style guidelines
2. Verifying that all tests pass
3. Ensuring the documentation is updated
4. Checking that the changes meet the project's goals

## Recognition

All contributors will be recognized in the project's documentation. We appreciate your contributions!

## Questions

If you have any questions about contributing, please create an issue or contact the project maintainers.

Thank you for contributing to the Task Manager project!