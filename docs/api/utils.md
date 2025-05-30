# Utilities API Reference

This document provides detailed information about the utility modules used in the Task Manager application.

## Exceptions

The Task Manager application defines custom exceptions to handle specific error cases. These exceptions are defined in `src/utils/exceptions.py`.

### Class Hierarchy

```
Exception
└── TaskManagerException
    ├── TaskNotFoundException
    └── InvalidTaskDataException
```

### TaskManagerException

Base exception for all task manager exceptions.

```python
class TaskManagerException(Exception):
    pass
```

This is the parent class for all custom exceptions in the Task Manager application. It inherits from the built-in `Exception` class and doesn't add any additional functionality.

**Usage:**
```python
try:
    # Some operation that might raise a TaskManagerException
    pass
except TaskManagerException as e:
    print(f"A task manager error occurred: {e}")
```

### TaskNotFoundException

Exception raised when a task is not found.

```python
class TaskNotFoundException(TaskManagerException):
    pass
```

This exception is raised when attempting to access a task that doesn't exist, typically by its ID.

**Usage:**
```python
try:
    task = task_service.get_task_by_id(999)  # Assuming task with ID 999 doesn't exist
except TaskNotFoundException as e:
    print(f"Error: {e}")  # "Error: Task with ID 999 not found"
```

**Where it's raised:**
- `TaskService.get_task_by_id()`: When no task with the given ID exists
- `TaskService.update_task()`: When no task with the given ID exists
- `TaskService.complete_task()`: When no task with the given ID exists
- `TaskService.delete_task()`: When no task with the given ID exists

### InvalidTaskDataException

Exception raised when task data is invalid.

```python
class InvalidTaskDataException(TaskManagerException):
    pass
```

This exception is intended to be raised when task data doesn't meet the required format or constraints, although it's not currently used in the application.

**Potential usage:**
```python
def validate_task_data(data):
    if not data.get("title"):
        raise InvalidTaskDataException("Task title is required")
    if data.get("priority") not in ["low", "medium", "high"]:
        raise InvalidTaskDataException("Invalid priority value")
```

## Best Practices for Exception Handling

When working with the Task Manager application, it's recommended to handle exceptions as follows:

### Specific to General Exception Handling

```python
try:
    # Some operation that might raise exceptions
    task = task_service.get_task_by_id(task_id)
except TaskNotFoundException as e:
    # Handle the specific case where the task is not found
    print(f"Error: {e}")
except TaskManagerException as e:
    # Handle other task manager exceptions
    print(f"Task manager error: {e}")
except Exception as e:
    # Handle any other unexpected exceptions
    print(f"Unexpected error: {e}")
```

### Using Exception Information

```python
try:
    task = task_service.get_task_by_id(task_id)
except TaskNotFoundException as e:
    # Use the exception message in the error handling
    print(f"Could not find the requested task: {e}")
    # You might want to log the error or display a user-friendly message
    logging.error(f"Task not found: {task_id}")
    # Maybe suggest alternatives
    similar_tasks = task_service.search_tasks(f"Task {task_id}")
    if similar_tasks:
        print("Did you mean one of these tasks?")
        for task in similar_tasks:
            print(f"- {task}")
```

### In CLI Applications

In command-line applications, you might want to handle exceptions by displaying user-friendly error messages and setting appropriate exit codes:

```python
try:
    # Some operation that might raise exceptions
    task = task_service.get_task_by_id(task_id)
except TaskNotFoundException as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)  # Exit with a non-zero status code to indicate an error
```

### In Web Applications

In web applications, you might want to handle exceptions by returning appropriate HTTP status codes and error messages:

```python
@app.route("/tasks/<int:task_id>")
def get_task(task_id):
    try:
        task = task_service.get_task_by_id(task_id)
        return jsonify(task.to_dict())
    except TaskNotFoundException:
        return jsonify({"error": f"Task with ID {task_id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

## Future Enhancements

Potential future enhancements to the exceptions module could include:

- More specific exception types for different error cases
- Additional validation exceptions for different types of invalid data
- Exception handling utilities to standardize error responses
- Integration with a logging system for better error tracking