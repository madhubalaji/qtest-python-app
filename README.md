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

Run the tests:

```
pytest
```

Run tests with coverage:

```
pytest --cov=src --cov-report=html
```

## Code Quality

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **pytest**: Testing with coverage

To run all quality checks locally:

```bash
# Format code
black .
isort .

# Check formatting (without making changes)
black --check .
isort --check-only .

# Lint code
flake8 .

# Run tests with coverage
pytest --cov=src --cov-report=term-missing
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment. The pipeline includes:

### Test Job
- **Multi-version testing**: Tests run on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- **Code quality checks**: Black formatting, isort import sorting, and flake8 linting
- **Test coverage**: Comprehensive test coverage with reporting
- **Dependency caching**: Pip dependencies are cached for faster builds

### Build Job
- **Package building**: Creates distributable packages
- **Package validation**: Validates package integrity with twine
- **Artifact upload**: Stores build artifacts for potential deployment
- **Conditional execution**: Only runs on main branch after successful tests

### Workflow Triggers
- **Push events**: Triggers on pushes to any branch
- **Pull requests**: Triggers on pull requests to any branch
- **Manual dispatch**: Can be triggered manually from GitHub interface

The workflow ensures that:
1. All code changes are properly tested across multiple Python versions
2. Code style and quality standards are maintained
3. Test coverage is tracked and reported
4. Packages can be built successfully before deployment

## License

[MIT License](LICENSE)
