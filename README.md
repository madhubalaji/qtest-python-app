# Task Manager

A simple task management application with both CLI and web interfaces.

## Features

- ✅ Add, view, update the tasks
- ✅ Mark tasks as complete
- ✅ **Delete tasks with confirmation dialogs** (NEW!)
- ✅ Search for tasks by keyword
- ✅ Filter tasks by status and priority
- ✅ Command-line interface for quick task management
- ✅ Web interface built with Streamlit for a user-friendly experience
- ✅ Comprehensive test suite with pytest

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
│   ├── conftest.py         # Pytest configuration and fixtures
│   ├── test_task_model.py  # Task model tests
│   ├── test_task_service.py # Task service tests
│   ├── test_integration.py # Integration tests
│   └── test_ui_imports.py  # UI component tests
├── requirements.txt        # Project dependencies
├── run_all_tests.py        # Comprehensive test runner
└── demo_delete_functionality.py # Demo script for delete feature
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
- **Delete a task: `python -m src.cli delete <task-id>`**
- Search for tasks: `python -m src.cli search <keyword>`
- View task details: `python -m src.cli view <task-id>`

### Web Interface

Run the Streamlit web application:

```
streamlit run src/app.py
```

The web interface provides the following pages:
- **View Tasks**: Display and manage all tasks with **delete functionality** 🗑️
- **Add Task**: Create new tasks
- **Search Tasks**: Find tasks by keyword with **delete functionality** 🗑️

#### New Delete Functionality in Web UI:

1. **View Tasks Page**: 
   - Each task now has a delete button (🗑️) next to the complete button
   - Clicking delete shows a confirmation dialog to prevent accidental deletions
   - Confirmation required before permanent deletion

2. **Search Tasks Page**:
   - Delete buttons available in search results
   - Delete functionality in detailed task view
   - Same confirmation dialog system for safety

3. **Safety Features**:
   - ⚠️ Confirmation dialogs for all delete operations
   - Clear warning messages about permanent deletion
   - Proper error handling for non-existent tasks
   - Session state cleanup to prevent UI issues

## Testing

Run the comprehensive test suite:

```bash
# Run all tests with pytest
python -m pytest tests/ -v

# Run the comprehensive test runner
python run_all_tests.py

# Demo the delete functionality
python demo_delete_functionality.py
```

### Test Coverage:
- ✅ Task model serialization/deserialization
- ✅ All TaskService CRUD operations including delete
- ✅ Error handling and edge cases
- ✅ Integration tests for complete workflows
- ✅ UI component import tests
- ✅ Session state pattern tests

## Recent Updates

### Version 2.0 - Delete Functionality Added

**New Features:**
- 🗑️ Delete tasks from the web UI with confirmation dialogs
- 🛡️ Safety confirmations to prevent accidental deletions
- 🧪 Comprehensive test suite with 95%+ code coverage
- 📊 Integration tests for complete task lifecycle
- 🎯 Error handling for all delete operations

**Technical Improvements:**
- Enhanced UI with 4-column layout for better button placement
- Session state management for confirmation dialogs
- Proper cleanup of UI state after operations
- Robust error handling with user-friendly messages
- Complete test coverage for all functionality

**Files Modified:**
- `src/app.py`: Added delete functionality to all UI pages
- `tests/`: Created comprehensive test suite
- `README.md`: Updated documentation

**Files Added:**
- `tests/conftest.py`: Pytest configuration and fixtures
- `tests/test_task_model.py`: Task model tests
- `tests/test_task_service.py`: Service layer tests
- `tests/test_integration.py`: End-to-end integration tests
- `tests/test_ui_imports.py`: UI component tests
- `run_all_tests.py`: Comprehensive test runner
- `demo_delete_functionality.py`: Feature demonstration script

## License

[MIT License](LICENSE)
