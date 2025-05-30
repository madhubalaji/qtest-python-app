# Models API Reference

This document provides detailed information about the data models used in the Task Manager application.

## Task Model

The `Task` class represents a single task in the task management system. It is defined in `src/models/task.py`.

### Class Definition

```python
class Task:
    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        priority: str = "medium",
        completed: bool = False,
        created_at: Optional[str] = None
    ):
        # ...
```

### Constructor Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `task_id` | `int` | Unique identifier for the task | Required |
| `title` | `str` | Title of the task | Required |
| `description` | `str` | Detailed description of the task | `""` (empty string) |
| `priority` | `str` | Priority level (low, medium, high) | `"medium"` |
| `completed` | `bool` | Whether the task is completed | `False` |
| `created_at` | `Optional[str]` | Timestamp when the task was created | `None` (current timestamp will be used) |

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `int` | Unique identifier for the task |
| `title` | `str` | Title of the task |
| `description` | `str` | Detailed description of the task |
| `priority` | `str` | Priority level (low, medium, high) |
| `completed` | `bool` | Whether the task is completed |
| `created_at` | `str` | Timestamp when the task was created |

### Methods

#### `to_dict() -> Dict[str, Any]`

Converts the task to a dictionary representation.

**Returns:**
- `Dict[str, Any]`: Dictionary representation of the task

**Example:**
```python
task = Task(1, "Complete documentation")
task_dict = task.to_dict()
# Result: {"id": 1, "title": "Complete documentation", "description": "", "priority": "medium", "completed": False, "created_at": "2023-04-11 10:29:17"}
```

#### `from_dict(cls, data: Dict[str, Any]) -> 'Task'`

Class method that creates a Task instance from a dictionary.

**Parameters:**
- `data`: Dictionary containing task data

**Returns:**
- `Task`: A new Task instance

**Example:**
```python
task_data = {
    "id": 1,
    "title": "Complete documentation",
    "description": "Write comprehensive documentation",
    "priority": "high",
    "completed": False,
    "created_at": "2023-04-11 10:29:17"
}
task = Task.from_dict(task_data)
```

#### `__str__() -> str`

Returns a string representation of the task.

**Returns:**
- `str`: String representation of the task

**Example:**
```python
task = Task(1, "Complete documentation", priority="high")
str(task)  # "Task 1: Complete documentation (Active, high priority)"
```

### Usage Examples

#### Creating a Task

```python
# Create a task with minimal parameters
task1 = Task(1, "Complete documentation")

# Create a task with all parameters
task2 = Task(
    task_id=2,
    title="Write tests",
    description="Write comprehensive tests for the application",
    priority="high",
    completed=False
)
```

#### Converting Between Task and Dictionary

```python
# Convert a task to a dictionary
task = Task(1, "Complete documentation")
task_dict = task.to_dict()

# Create a task from a dictionary
new_task = Task.from_dict(task_dict)
```

#### String Representation

```python
task = Task(1, "Complete documentation", priority="high")
print(task)  # "Task 1: Complete documentation (Active, high priority)"

task.completed = True
print(task)  # "Task 1: Complete documentation (Completed, high priority)"
```

### Data Validation

The Task model does not currently perform validation on the input data. It is the responsibility of the caller to ensure that the data is valid. In particular:

- `task_id` should be a unique integer
- `title` should not be empty
- `priority` should be one of "low", "medium", or "high"
- `created_at` should be a string in the format "YYYY-MM-DD HH:MM:SS"

### Future Enhancements

Potential future enhancements to the Task model could include:

- Input validation
- Support for due dates
- Support for tags or categories
- Support for subtasks