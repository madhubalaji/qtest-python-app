# Task Manager

A simple task management application with both CLI and web interfaces.

## Features

- Add, view, update and **delete** tasks
- Mark tasks as complete
- Search for tasks by keyword
- Filter tasks by status and priority
- **Delete tasks with confirmation dialogs** (NEW!)
- Command-line interface for quick task management
- Web interface built with Streamlit for a user-friendly experience

## Project Structure

```
task_manager_project/
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
├── tests/                  # Test suite
│   ├── test_task_service.py # TaskService tests
│   ├── test_models.py      # Task model tests
│   └── test_exceptions.py  # Exception handling tests
├── requirements.txt        # Project dependencies
├── pytest.ini             # Pytest configuration
├── run_tests.py           # Test runner script
└── demo_delete_functionality.py # Delete functionality demo
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
- **View Tasks**: Display and manage all tasks with **delete functionality**
- **Add Task**: Create new tasks
- **Search Tasks**: Find tasks by keyword with **delete option in task details**

### New Delete Functionality

The web interface now includes comprehensive delete functionality:

#### In View Tasks Page:
- 🗑️ **Delete button** for each task
- **Confirmation dialog** before deletion
- **Success/error messages** for user feedback
- **Immediate UI refresh** after deletion

#### In Search Tasks Page:
- **Delete option** in task detail view
- **Confirmation dialog** with cancel option
- **Proper cleanup** of UI state after deletion

#### Safety Features:
- **Confirmation required** before any deletion
- **Error handling** for non-existent tasks
- **Clear user feedback** for all operations
- **Session state management** to prevent conflicts

## Testing

Run the test suite to verify functionality:

```bash
# Run all tests
python run_tests.py

# Or run pytest directly
pytest tests/ -v

# Demo the delete functionality
python demo_delete_functionality.py
```

The test suite includes:
- **TaskService tests**: Comprehensive testing of all CRUD operations including delete
- **Task model tests**: Validation of task creation and serialization
- **Exception handling tests**: Proper error handling verification
- **Integration tests**: End-to-end functionality validation



## License

[MIT License](LICENSE)
