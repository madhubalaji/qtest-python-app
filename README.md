# Task Manager

[![Python application](https://github.com/example/task-manager/actions/workflows/python-app.yml/badge.svg)](https://github.com/example/task-manager/actions/workflows/python-app.yml)
[![Security Scan](https://github.com/example/task-manager/actions/workflows/security.yml/badge.svg)](https://github.com/example/task-manager/actions/workflows/security.yml)
[![codecov](https://codecov.io/gh/example/task-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/example/task-manager)

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
│   └── test_task_service.py# Tests for TaskService
└── requirements.txt        # Project dependencies
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

Run the tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
```

Run specific test categories:

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests  
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Development

### Setting up development environment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd task_manager_project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Code Quality

The project uses several tools to maintain code quality:

- **pytest**: Testing framework with coverage reporting
- **flake8**: Code linting and style checking
- **black**: Code formatting
- **isort**: Import sorting
- **mypy**: Static type checking
- **bandit**: Security vulnerability scanning
- **safety**: Dependency vulnerability checking

Run all quality checks:

```bash
# Linting
flake8 src/ tests/

# Type checking
mypy src/

# Security scanning
bandit -r src/
safety check

# Code formatting (check only)
black --check src/ tests/
isort --check-only src/ tests/
```

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration with the following workflows:

1. **Main CI Pipeline** (`.github/workflows/python-app.yml`):
   - Tests across Python 3.9, 3.10, 3.11, and 3.12
   - Code linting with flake8
   - Test coverage reporting
   - Build artifact generation
   - Dependency caching for faster builds

2. **Security Scanning** (`.github/workflows/security.yml`):
   - Daily security scans
   - Dependency vulnerability checking
   - Static security analysis
   - SAST scanning with Semgrep

### Build and Packaging

Build the package:

```bash
python -m build
```

The built packages will be available in the `dist/` directory.

## License

[MIT License](LICENSE)
