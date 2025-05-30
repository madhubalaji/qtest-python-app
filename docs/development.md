# Development Guide

This guide provides information for developers who want to understand, modify, or extend the Task Manager application.

## Project Structure

The Task Manager project follows a modular structure:

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

## Development Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager
   ```

2. Create and activate a virtual environment:
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   venv\Scripts\activate     # On Windows
   
   # Or using conda
   conda create -n task-manager python=3.8
   conda activate task-manager
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

4. Install development dependencies:
   ```bash
   pip install pytest pytest-cov flake8 black isort
   ```

## Code Style Guidelines

The Task Manager project follows these code style guidelines:

- **PEP 8**: Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- **Docstrings**: Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for functions, methods, and classes.
- **Type Hints**: Use type hints for function and method signatures.
- **Line Length**: Limit lines to 88 characters (compatible with Black).

You can use the following tools to ensure code quality:

- **Black**: Code formatter
  ```bash
  black src tests
  ```

- **isort**: Import sorter
  ```bash
  isort src tests
  ```

- **flake8**: Linter
  ```bash
  flake8 src tests
  ```

## Testing

The Task Manager project uses pytest for testing. Tests are located in the `tests` directory.

### Running Tests

To run all tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=src
```

To generate a coverage report:

```bash
pytest --cov=src --cov-report=html
```

### Writing Tests

When adding new features or fixing bugs, make sure to write appropriate tests. Here's an example of a test for the `Task` model:

```python
import pytest
from src.models.task import Task

def test_task_creation():
    task = Task(1, "Test Task", "Test Description", "high")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "high"
    assert task.completed is False

def test_task_to_dict():
    task = Task(1, "Test Task")
    task_dict = task.to_dict()
    assert task_dict["id"] == 1
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == ""
    assert task_dict["priority"] == "medium"
    assert task_dict["completed"] is False
    assert "created_at" in task_dict
```

## Adding New Features

When adding new features to the Task Manager application, follow these steps:

1. **Create an issue**: Describe the feature you want to add.
2. **Create a branch**: Create a new branch for your feature.
3. **Implement the feature**: Write the code for your feature.
4. **Write tests**: Write tests for your feature.
5. **Update documentation**: Update the documentation to reflect your changes.
6. **Submit a pull request**: Submit a pull request for review.

### Example: Adding a Due Date Feature

Here's an example of how you might add a due date feature to the Task Manager application:

1. Update the `Task` model in `src/models/task.py`:
   ```python
   def __init__(
       self,
       task_id: int,
       title: str,
       description: str = "",
       priority: str = "medium",
       completed: bool = False,
       created_at: Optional[str] = None,
       due_date: Optional[str] = None  # Add due_date parameter
   ):
       self.id = task_id
       self.title = title
       self.description = description
       self.priority = priority
       self.completed = completed
       self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       self.due_date = due_date  # Store due_date
   ```

2. Update the `to_dict` and `from_dict` methods to include the due date.

3. Update the `TaskService` class to support due dates in the `add_task` and `update_task` methods.

4. Update the CLI and web interface to allow setting and displaying due dates.

5. Write tests for the new functionality.

6. Update the documentation to reflect the changes.

## Debugging

### CLI Debugging

For debugging the CLI application, you can use the Python debugger:

```bash
python -m pdb src/cli.py [command] [arguments]
```

### Web Interface Debugging

For debugging the web interface, you can use Streamlit's built-in debugging features:

1. Run the application with the `--logger.level=debug` flag:
   ```bash
   streamlit run src/app.py --logger.level=debug
   ```

2. Use `st.write` to display debug information in the web interface:
   ```python
   st.write("Debug:", variable)
   ```

## Deployment

### CLI Application

To deploy the CLI application, you can create a distributable package:

```bash
python setup.py sdist bdist_wheel
```

This will create a distributable package in the `dist` directory.

### Web Application

To deploy the web application, you can use Streamlit's deployment options:

1. **Streamlit Sharing**: Deploy directly from GitHub to [Streamlit Sharing](https://streamlit.io/sharing).

2. **Docker**: Create a Docker container for the application:
   ```dockerfile
   FROM python:3.8-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "src/app.py"]
   ```

   Build and run the Docker container:
   ```bash
   docker build -t task-manager .
   docker run -p 8501:8501 task-manager
   ```

## Performance Considerations

The Task Manager application uses a simple JSON file for storage, which is suitable for small to medium-sized task lists. For larger task lists or multi-user scenarios, consider the following optimizations:

1. **Database Storage**: Replace the JSON file storage with a database (e.g., SQLite, PostgreSQL).

2. **Caching**: Implement caching for frequently accessed tasks.

3. **Pagination**: Implement pagination for large task lists.

## Security Considerations

The Task Manager application is designed for personal use and doesn't include authentication or authorization features. If you plan to use it in a multi-user environment, consider adding:

1. **Authentication**: Add user authentication to protect user data.

2. **Authorization**: Add authorization to control access to tasks.

3. **Input Validation**: Add more robust input validation to prevent security vulnerabilities.

## Contributing

Please see the [Contributing Guidelines](contributing.md) for information on how to contribute to the Task Manager project.