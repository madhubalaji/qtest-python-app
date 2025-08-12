# Task Manager

A simple task management application with both CLI and web interfaces.

## Features

- Add, view, update, and delete tasks
- Mark tasks as complete
- Search for tasks by keyword
- Filter tasks by status and priority
- Delete tasks with confirmation dialog
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
│   ├── test_task_service.py# Tests for TaskService
│   └── test_integration.py # Integration tests
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
- **View Tasks**: Display and manage all tasks with delete functionality
- **Add Task**: Create new tasks
- **Search Tasks**: Find tasks by keyword with delete option in task details

### Delete Functionality

The application now includes comprehensive delete functionality:

#### Web Interface:
- **Delete buttons** (🗑️) are available in the task list view
- **Confirmation dialog** prevents accidental deletions
- **Delete option** in task details view when searching
- **Success/error messages** provide user feedback

#### Command Line Interface:
- Use `python -m src.cli delete <task-id>` to delete tasks
- Includes confirmation prompts for safety

## Testing

Run the complete test suite:

```bash
pytest
```

Run specific test files:

```bash
# Test the Task model
pytest tests/test_task_model.py

# Test the TaskService
pytest tests/test_task_service.py

# Test integration scenarios
pytest tests/test_integration.py
```

Run a quick functionality test:

```bash
python run_tests.py
```

The test suite includes:
- **Unit tests** for Task model and TaskService
- **Integration tests** for complete workflows
- **Delete functionality tests** with error handling
- **Persistence tests** to ensure data integrity

## License

[MIT License](LICENSE)
