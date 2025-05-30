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
│   ├── index.md            # Main documentation page
│   ├── installation.md     # Installation instructions
│   ├── usage/              # Usage guides
│   │   ├── cli.md          # CLI usage guide
│   │   └── web.md          # Web interface usage guide
│   ├── api/                # API reference
│   │   ├── models.md       # Models documentation
│   │   ├── services.md     # Services documentation
│   │   └── utils.md        # Utilities documentation
│   ├── development.md      # Development guide
│   └── contributing.md     # Contributing guidelines
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

For detailed installation instructions, see the [Installation Guide](docs/installation.md).

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

For detailed CLI usage instructions, see the [CLI Documentation](docs/usage/cli.md).

### Web Interface

Run the Streamlit web application:

```
streamlit run src/app.py
```

The web interface provides the following pages:
- View Tasks: Display and manage all tasks
- Add Task: Create new tasks
- Search Tasks: Find tasks by keyword

For detailed web interface usage instructions, see the [Web Interface Documentation](docs/usage/web.md).

## Documentation

Comprehensive documentation is available in the `docs` directory:

- [Main Documentation](docs/index.md): Overview and quick start guide
- [Installation Guide](docs/installation.md): Detailed installation instructions
- Usage Guides:
  - [Command-line Interface](docs/usage/cli.md): How to use the CLI
  - [Web Interface](docs/usage/web.md): How to use the web interface
- API Reference:
  - [Models](docs/api/models.md): Documentation for data models
  - [Services](docs/api/services.md): Documentation for services
  - [Utilities](docs/api/utils.md): Documentation for utilities
- [Development Guide](docs/development.md): Guide for developers
- [Contributing Guidelines](docs/contributing.md): Guidelines for contributing to the project

## Testing

Run the tests:

```
pytest
```

## Contributing

Contributions are welcome! Please see the [Contributing Guidelines](docs/contributing.md) for more information.

## License

[MIT License](LICENSE)
