# Services API Reference

This document provides detailed information about the service classes used in the Task Manager application.

## TaskService

The `TaskService` class provides methods for managing tasks, including adding, retrieving, updating, and deleting tasks. It is defined in `src/services/task_service.py`.

### Class Definition

```python
class TaskService:
    def __init__(self, storage_file: str = "tasks.json"):
        # ...
```

### Constructor Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `storage_file` | `str` | Path to the JSON file for storing tasks | `"tasks.json"` |

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `storage_file` | `str` | Path to the JSON file for storing tasks |
| `tasks` | `List[Task]` | List of Task objects loaded from the storage file |

### Methods

#### `_load_tasks() -> List[Task]`

Private method that loads tasks from the storage file.

**Returns:**
- `List[Task]`: List of Task objects

#### `_save_tasks() -> None`

Private method that saves tasks to the storage file.

#### `add_task(title: str, description: str = "", priority: str = "medium") -> Task`

Adds a new task.

**Parameters:**
- `title`: Task title
- `description`: Task description (default: `""`)
- `priority`: Task priority (default: `"medium"`)

**Returns:**
- `Task`: The newly created Task

**Example:**
```python
task_service = TaskService("tasks.json")
new_task = task_service.add_task(
    title="Complete documentation",
    description="Write comprehensive documentation",
    priority="high"
)
```

#### `get_all_tasks(show_completed: bool = True) -> List[Task]`

Gets all tasks, optionally filtering out completed tasks.

**Parameters:**
- `show_completed`: Whether to include completed tasks (default: `True`)

**Returns:**
- `List[Task]`: List of Task objects

**Example:**
```python
task_service = TaskService("tasks.json")

# Get all tasks
all_tasks = task_service.get_all_tasks()

# Get only active tasks
active_tasks = task_service.get_all_tasks(show_completed=False)
```

#### `get_task_by_id(task_id: int) -> Task`

Gets a task by its ID.

**Parameters:**
- `task_id`: ID of the task to retrieve

**Returns:**
- `Task`: The requested Task

**Raises:**
- `TaskNotFoundException`: If no task with the given ID exists

**Example:**
```python
task_service = TaskService("tasks.json")
try:
    task = task_service.get_task_by_id(1)
    print(f"Found task: {task}")
except TaskNotFoundException as e:
    print(f"Error: {e}")
```

#### `update_task(task_id: int, **kwargs) -> Task`

Updates a task with the given ID.

**Parameters:**
- `task_id`: ID of the task to update
- `**kwargs`: Task attributes to update (can include `title`, `description`, `priority`, `completed`)

**Returns:**
- `Task`: The updated Task

**Raises:**
- `TaskNotFoundException`: If no task with the given ID exists

**Example:**
```python
task_service = TaskService("tasks.json")
updated_task = task_service.update_task(
    task_id=1,
    title="Updated title",
    description="Updated description",
    priority="low"
)
```

#### `complete_task(task_id: int) -> Task`

Marks a task as complete.

**Parameters:**
- `task_id`: ID of the task to mark as complete

**Returns:**
- `Task`: The updated Task

**Raises:**
- `TaskNotFoundException`: If no task with the given ID exists

**Example:**
```python
task_service = TaskService("tasks.json")
completed_task = task_service.complete_task(1)
```

#### `delete_task(task_id: int) -> Task`

Deletes a task.

**Parameters:**
- `task_id`: ID of the task to delete

**Returns:**
- `Task`: The deleted Task

**Raises:**
- `TaskNotFoundException`: If no task with the given ID exists

**Example:**
```python
task_service = TaskService("tasks.json")
deleted_task = task_service.delete_task(1)
```

#### `search_tasks(keyword: str) -> List[Task]`

Searches for tasks containing the keyword in their title or description.

**Parameters:**
- `keyword`: Keyword to search for in task titles and descriptions

**Returns:**
- `List[Task]`: List of matching Task objects

**Example:**
```python
task_service = TaskService("tasks.json")
matching_tasks = task_service.search_tasks("documentation")
```

### Usage Examples

#### Complete Task Management Workflow

```python
# Initialize the task service
task_service = TaskService("tasks.json")

# Add a new task
task = task_service.add_task(
    title="Complete documentation",
    description="Write comprehensive documentation",
    priority="high"
)
print(f"Added task: {task}")

# Get all tasks
all_tasks = task_service.get_all_tasks()
print(f"All tasks: {all_tasks}")

# Update a task
updated_task = task_service.update_task(
    task_id=task.id,
    description="Write comprehensive documentation for the project"
)
print(f"Updated task: {updated_task}")

# Mark a task as complete
completed_task = task_service.complete_task(task.id)
print(f"Completed task: {completed_task}")

# Search for tasks
matching_tasks = task_service.search_tasks("documentation")
print(f"Matching tasks: {matching_tasks}")

# Delete a task
deleted_task = task_service.delete_task(task.id)
print(f"Deleted task: {deleted_task}")
```

### Error Handling

The `TaskService` class raises the following exceptions:

- `TaskNotFoundException`: When a task with the specified ID is not found
- `json.JSONDecodeError`: When the storage file contains invalid JSON data

It is recommended to handle these exceptions appropriately in your code.

### Thread Safety

The `TaskService` class is not thread-safe. If you need to use it in a multi-threaded environment, you should implement appropriate synchronization mechanisms.

### Storage Format

Tasks are stored in a JSON file with the following format:

```json
[
  {
    "id": 1,
    "title": "Complete documentation",
    "description": "Write comprehensive documentation",
    "priority": "high",
    "completed": false,
    "created_at": "2023-04-11 10:29:17"
  },
  {
    "id": 2,
    "title": "Write tests",
    "description": "Write comprehensive tests for the application",
    "priority": "medium",
    "completed": true,
    "created_at": "2023-04-11 10:30:00"
  }
]
```