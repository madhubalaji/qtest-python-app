# Task Manager

A simple task management application with both CLI and web interfaces.

[![CI/CD Pipeline](https://github.com/yourusername/task-manager/actions/workflows/python-app.yml/badge.svg)](https://github.com/yourusername/task-manager/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/yourusername/task-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/task-manager)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
│   ├── test_cli.py         # Tests for CLI interface
│   └── test_exceptions.py  # Tests for custom exceptions
├── requirements.txt        # Project dependencies
├── pyproject.toml          # Project configuration
├── pytest.ini             # Test configuration
└── setup.py               # Package setup
```

## Installation

### For Users

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd task_manager_project
   ```

2. Install the package:
   ```bash
   pip install .
   ```

### For Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd task_manager_project
   ```

2. Install in development mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

### Command-line Interface

After installation, you can use the CLI directly:

```bash
task-manager --help
```

Or run it as a module:

```bash
python -m src.cli
```

Available commands:

- Add a task: `task-manager add "Task title" -d "Task description" -p high`
- List tasks: `task-manager list`
- List all tasks including completed: `task-manager list -a`
- Complete a task: `task-manager complete <task-id>`
- Delete a task: `task-manager delete <task-id>`
- Search for tasks: `task-manager search <keyword>`
- View task details: `task-manager view <task-id>`

### Web Interface

Run the Streamlit web application:

```bash
streamlit run src/app.py
```

The web interface provides the following pages:
- View Tasks: Display and manage all tasks
- Add Task: Create new tasks
- Search Tasks: Find tasks by keyword

## Development

### Testing

Run the full test suite:

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
pytest tests/test_cli.py
```

### Code Quality

Format code with Black:

```bash
black src/ tests/
```

Sort imports with isort:

```bash
isort src/ tests/
```

Lint with flake8:

```bash
flake8 src/ tests/
```

Security analysis with Bandit:

```bash
bandit -r src/
```

Check for dependency vulnerabilities:

```bash
safety check
```

### CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment. The pipeline includes:

#### Code Quality & Security
- Code formatting checks (Black)
- Import sorting checks (isort)
- Linting (flake8)
- Security analysis (Bandit)
- Dependency vulnerability scanning (Safety)
- CodeQL security analysis

#### Testing
- Matrix testing across Python 3.8, 3.9, 3.10, 3.11, 3.12
- Multi-platform testing (Ubuntu, Windows, macOS)
- Test coverage reporting
- Artifact uploads for test results and coverage reports

#### Build & Distribution
- Package building (wheel and source distribution)
- Distribution validation
- Integration testing
- Deployment readiness checks

#### Artifacts
The CI pipeline generates and stores the following artifacts:
- **Test Results**: JUnit XML files and HTML coverage reports
- **Security Reports**: Bandit and Safety scan results
- **Distribution Packages**: Built wheel and source distributions

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite (`pytest`)
5. Run code quality checks (`black src/ tests/ && isort src/ tests/ && flake8 src/ tests/`)
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Supported Python Versions

This project supports Python 3.8 and above. The CI pipeline tests against:
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

### Dependencies

#### Runtime Dependencies
- `streamlit>=1.22.0` - Web interface framework

#### Development Dependencies
- `pytest>=7.3.1` - Testing framework
- `pytest-cov>=4.1.0` - Coverage plugin for pytest
- `coverage>=7.2.0` - Coverage measurement
- `black>=23.0.0` - Code formatter
- `isort>=5.12.0` - Import sorter
- `bandit>=1.7.5` - Security linter
- `safety>=2.3.0` - Dependency vulnerability scanner
- `flake8>=6.0.0` - Code linter

## License

[MIT License](LICENSE)
