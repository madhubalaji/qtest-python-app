# Task Manager

A simple task management application with both CLI and web interfaces.

## Features

- Add, view, update, and delete tasks
- Mark tasks as complete
- Search for tasks by keyword
- Filter tasks by status and priority
- Delete tasks with confirmation dialogs (web interface)
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
- **View Tasks**: Display and manage all tasks with delete functionality
- **Add Task**: Create new tasks
- **Search Tasks**: Find tasks by keyword with delete option in task details

### Delete Functionality

The web interface now includes delete functionality with safety features:

#### In View Tasks Page:
1. Click the trash can icon (🗑️) next to any task
2. Confirm deletion by clicking "Yes" in the confirmation dialog
3. Cancel by clicking "No" if you change your mind

#### In Search Tasks Page:
1. Search for and select a task to view its details
2. Click the "🗑️ Delete" button in the task details view
3. Confirm the deletion when prompted

**Safety Features:**
- All deletions require explicit confirmation
- Clear visual feedback during the confirmation process
- Easy cancellation option
- Automatic UI refresh after successful deletion

## Testing

Run the tests:

```
pytest
```

## License

[MIT License](LICENSE)
