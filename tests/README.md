# Task Manager Tests

This directory contains tests for the Task Manager application.

## Test Structure

- `test_task_model.py`: Tests for the Task model
- `test_task_service.py`: Tests for the TaskService class
- `test_cli.py`: Tests for the command-line interface
- `test_app.py`: Tests for the Streamlit web application
- `test_exceptions.py`: Tests for the custom exceptions

## Running Tests

To run all tests:

```bash
pytest
```

To run tests with coverage report:

```bash
pytest --cov=src --cov-report=term-missing
```

To run a specific test file:

```bash
pytest tests/test_task_model.py
```

To run a specific test:

```bash
pytest tests/test_task_model.py::TestTaskModel::test_task_initialization
```

## Test Fixtures

Common test fixtures are defined in `conftest.py`:

- `sample_tasks`: A list of sample Task objects
- `temp_storage_file`: A temporary file for task storage
- `task_service`: A TaskService instance with a temporary storage file
- `mock_task_service`: A mock TaskService object