# Task Manager

A simple task management application with both CLI and web interfaces.

## Features

- Add, view, update the tasks
- Mark tasks as complete
- **Delete tasks with confirmation dialog** (New Feature)
- Search for tasks by keyword
- Filter tasks by status and priority
- Command-line interface for quick task management
- Web interface built with Streamlit for a user-friendly experience
- **Hindi language support in UI** (Enhanced Feature)

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
- **View Tasks (कार्य देखें)**: Display and manage all tasks with delete functionality
- **Add Task (कार्य जोड़ें)**: Create new tasks
- **Search Tasks (कार्य खोजें)**: Find tasks by keyword with delete options

### New Delete Functionality

The web interface now includes comprehensive delete functionality:

1. **Delete Button**: Each task displays a delete button (🗑️) in the task list
2. **Confirmation Dialog**: Two-step confirmation process prevents accidental deletions
3. **Multiple Locations**: Delete functionality available in:
   - Main task view page
   - Search results
   - Task detail view
4. **Hindi Language Support**: All UI elements translated to Hindi for better accessibility



## License

[MIT License](LICENSE)
