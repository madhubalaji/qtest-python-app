# Task Manager

A simple task management application with both CLI and web interfaces.

## Features

- Add, view, update the tasks
- Mark tasks as complete
- Search for tasks by keyword
- Filter tasks by status and priority
- Command-line interface for quick task management
- Web interface built with Streamlit for a user-friendly experience

## Project Structure

```
task_manager_project/
├── .github/                # GitHub Actions workflows
│   └── workflows/
│       └── python-app.yml  # CI/CD pipeline
├── config/                 # Configuration files and task storage
├── docs/                   # Documentation
├── src/                    # Source code
│   ├── models/             # Data models
│   │   └── task.py         # Task model
│   ├── services/           # Business logic
│   │   └── task_service.py # Task management service
│   ├── utils/              # Utility modules
│   │   └── exceptions.py   # Custom exceptions
│   ├── app.py              # Streamlit web application
│   └── cli.py              # Command-line interface
├── tests/                  # Test cases
│   ├── test_task_model.py  # Tests for Task model
│   ├── test_task_service.py# Tests for TaskService
│   └── test_integration.py # Integration tests
├── requirements.txt        # Project dependencies
├── requirements-dev.txt    # Development dependencies
├── pytest.ini            # Pytest configuration
├── MANIFEST.in            # Package manifest
└── run_tests.py           # Local test runner
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd task_manager_project
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. For development, install additional dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

## Usage

### Command-line Interface

Run the CLI application:

```
python -m src.cli
```

Available commands:

- Add a task: `python -m src.cli add "Task title" -d "Task description" -p high`
- List tasks: `python -m src.cli list`
- List all tasks including completed: `python -m src.cli list -a`
- Complete a task: `python -m src.cli complete <task-id>`
- Delete a task: `python -m src.cli delete <task-id>`
- Search for tasks: `python -m src.cli search <keyword>`
- View task details: `python -m src.cli view <task-id>`

### Web Interface

Run the Streamlit web application:

```
streamlit run src/app.py
```

The web interface provides the following pages:
- View Tasks: Display and manage all tasks
- Add Task: Create new tasks
- Search Tasks: Find tasks by keyword

## Testing

### Running Tests Locally

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src --cov-report=html
```

Run specific test files:
```bash
pytest tests/test_task_model.py
pytest tests/test_task_service.py
pytest tests/test_integration.py
```

Use the test runner script:
```bash
python run_tests.py
```

### Test Structure

- **Unit Tests**: Test individual components in isolation
  - `test_task_model.py`: Tests for the Task model class
  - `test_task_service.py`: Tests for the TaskService class
- **Integration Tests**: Test component interactions
  - `test_integration.py`: CLI and application integration tests

### Coverage Requirements

The project maintains a minimum code coverage of 85%. Coverage reports are generated in:
- HTML format: `htmlcov/index.html`
- XML format: `coverage.xml`
- Terminal output with missing lines

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment. The workflow includes:

### Automated Testing
- **Multi-version Testing**: Tests run on Python 3.8, 3.9, 3.10, and 3.11
- **Unit Tests**: Comprehensive test suite with pytest
- **Code Coverage**: Automated coverage reporting with minimum thresholds
- **Integration Tests**: CLI and application functionality validation

### Code Quality Checks
- **Linting**: Code style validation with flake8
- **Security Scanning**: 
  - Bandit for Python security issues
  - Safety for dependency vulnerabilities
  - Trivy for comprehensive security scanning
- **Package Validation**: Build and distribution checks

### Artifact Management
- **Test Results**: JUnit XML reports for all Python versions
- **Coverage Reports**: HTML and XML coverage reports
- **Security Reports**: JSON reports from security scans
- **Build Artifacts**: Python package distributions

### Workflow Triggers
- **Push Events**: Runs on pushes to `main` and `develop` branches
- **Pull Requests**: Runs on PRs targeting `main` branch
- **Security Scans**: Additional security checks on push events

### Quality Gates
The pipeline enforces quality gates that must pass:
- All unit tests must pass across all Python versions
- Code coverage must meet minimum thresholds (85%)
- No high-severity security vulnerabilities
- Code style checks must pass
- Package must build successfully

### Workflow Jobs

1. **Test Job**: Runs tests across multiple Python versions with caching
2. **Build Job**: Validates package building and distribution
3. **Integration Test Job**: Tests CLI functionality and package installation
4. **Security Scan Job**: Comprehensive security vulnerability scanning
5. **Quality Gate Job**: Final validation of all quality requirements

## Development

### Setting up Development Environment

1. Clone the repository
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Run tests to verify setup: `python run_tests.py`

### Code Style

The project follows PEP 8 style guidelines. Use flake8 for linting:
```bash
flake8 src/ tests/
```

### Security

Security is validated through multiple tools:
- **Bandit**: Scans for common security issues in Python code
- **Safety**: Checks dependencies for known vulnerabilities
- **Trivy**: Comprehensive vulnerability scanning

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python run_tests.py`
5. Submit a pull request

The CI/CD pipeline will automatically run all tests and quality checks on your pull request.

## License

[MIT License](LICENSE)
