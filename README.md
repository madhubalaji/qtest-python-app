# Task Manager

A simple task management application with both CLI and web interfaces.

## Features

- Add, view, update the tasks
- Mark tasks as complete
- **Delete tasks with confirmation dialog** ✨ *New Feature*
- Search for tasks by keyword
- Filter tasks by status and priority
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
├── tests/                  # Unit and integration tests
│   ├── test_task_service.py    # TaskService tests
│   └── test_app_integration.py # Integration tests
├── requirements.txt        # Project dependencies
└── run_tests.py           # Test runner script
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
- **View Tasks**: Display and manage all tasks with delete functionality 🗑️
- **Add Task**: Create new tasks
- **Search Tasks**: Find tasks by keyword with delete option in task details

#### 🗑️ Delete Task Feature

The new delete functionality is available in two locations:

1. **View Tasks Page**:
   - Click the 🗑️ (trash) button next to any task
   - Confirm deletion in the warning dialog
   - Task is permanently removed from the list

2. **Search Tasks Page**:
   - Search for a task and click "View" to see details
   - Click "Delete Task" button in the task details view
   - Confirm deletion in the warning dialog

**Important Notes**:
- ⚠️ Deletion is permanent and cannot be undone
- 🔒 Confirmation dialog prevents accidental deletions
- ✅ Works for both completed and active tasks
- 💾 Changes are immediately saved to storage

## Testing

Run the test suite to verify functionality:

```
python run_tests.py
```

Or run individual test files:

```
python -m pytest tests/test_task_service.py
python -m pytest tests/test_app_integration.py
```

## Demo

To see the delete feature in action:

```
python demo_delete_feature.py
```

This will show current tasks and explain how to use the delete functionality.

## License

[MIT License](LICENSE)
