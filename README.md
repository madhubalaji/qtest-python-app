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

The project includes comprehensive unit and integration tests.

### Running Tests Locally

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

Run specific test files:
```bash
pytest tests/test_task_model.py
pytest tests/test_task_service.py
pytest tests/test_integration.py
```

### Test Structure

- `tests/test_task_model.py` - Unit tests for the Task model
- `tests/test_task_service.py` - Unit tests for the TaskService class
- `tests/test_integration.py` - Integration tests for complete workflows
- `tests/conftest.py` - Shared test configuration and fixtures

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

#### Workflow Features

- **Multi-Python Testing**: Tests run on Python 3.9, 3.10, and 3.11
- **Dependency Caching**: Pip dependencies are cached for faster builds
- **Code Linting**: Flake8 linting with syntax error detection
- **Test Coverage**: Coverage reports generated with pytest-cov
- **Test Artifacts**: HTML test reports and coverage reports uploaded as artifacts
- **Package Building**: Automatic package building for main branch pushes
- **Codecov Integration**: Coverage reports sent to Codecov for tracking

#### Workflow Jobs

1. **Test Job**: Runs on all Python versions
   - Installs dependencies
   - Runs flake8 linting
   - Executes pytest with coverage
   - Uploads test results and coverage reports as artifacts

2. **Build Job**: Runs only on main branch pushes
   - Builds the Python package
   - Uploads distribution artifacts

#### Artifacts

The workflow generates the following artifacts:
- `test-results-{python-version}`: HTML test reports and coverage data
- `python-package-distributions`: Built Python packages (wheels and source distributions)

All artifacts are retained for 30-90 days and can be downloaded from the GitHub Actions interface.

## License

[MIT License](LICENSE)
