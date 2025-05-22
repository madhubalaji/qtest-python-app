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

## Development

This project includes a Makefile with several useful commands for development:

```
make help           # Show available commands
make test           # Run tests
make test-cov       # Run tests with coverage report
make lint           # Run linting
make build          # Build the package
make install        # Install the package in development mode
make clean          # Clean build artifacts
```

### Pre-push Hook

A pre-push hook script is provided to run tests before pushing changes. To use it:

1. Copy the script to your local Git hooks directory:
   ```
   cp pre-push.sh .git/hooks/pre-push
   chmod +x .git/hooks/pre-push
   ```

2. Now tests will run automatically before each push, preventing pushes if tests fail.

## Testing

Run the tests:

```
pytest
```

To run tests with coverage report:

```
pytest --cov=src
```

## Continuous Integration

This project uses GitHub Actions for continuous integration. The workflow automatically runs on push to main, develop, feature/*, and release/* branches, as well as on pull requests to main and develop.

The CI workflow performs the following tasks:
- Installs dependencies
- Runs linting with flake8
- Runs tests with pytest
- Generates test coverage reports
- Builds the Python package
- Verifies the package installation

You can view the workflow configuration in `.github/workflows/python-app.yml`.

### Running CI Locally

You can run the CI workflow locally to test your changes before pushing:

```
chmod +x run_ci_locally.sh
./run_ci_locally.sh
```

This script will run the same steps as the GitHub Actions workflow.

## License

[MIT License](LICENSE)
