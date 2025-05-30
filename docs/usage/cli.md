# Command-line Interface Documentation

The Task Manager provides a comprehensive command-line interface (CLI) for managing tasks directly from your terminal.

## Getting Started

To use the CLI, you can run:

```bash
python -m src.cli [command] [arguments]
```

Or, if you installed the package:

```bash
task-manager [command] [arguments]
```

If you run the command without any arguments, it will display the help message with available commands.

## Available Commands

### Add a Task

Add a new task to your task list.

```bash
python -m src.cli add "Task title" [-d "Task description"] [-p priority]
```

**Arguments:**
- `"Task title"`: The title of the task (required)
- `-d, --description "Task description"`: A detailed description of the task (optional)
- `-p, --priority priority`: The priority level of the task (optional, choices: "low", "medium", "high", default: "medium")

**Example:**
```bash
python -m src.cli add "Complete project documentation" -d "Write comprehensive documentation for the project" -p high
```

### List Tasks

List all tasks in your task list.

```bash
python -m src.cli list [-a]
```

**Arguments:**
- `-a, --all`: Show completed tasks as well (optional, by default only active tasks are shown)

**Example:**
```bash
python -m src.cli list -a
```

### Complete a Task

Mark a task as complete.

```bash
python -m src.cli complete <task-id>
```

**Arguments:**
- `<task-id>`: The ID of the task to mark as complete (required)

**Example:**
```bash
python -m src.cli complete 1
```

### Delete a Task

Delete a task from your task list.

```bash
python -m src.cli delete <task-id>
```

**Arguments:**
- `<task-id>`: The ID of the task to delete (required)

**Example:**
```bash
python -m src.cli delete 1
```

### Search for Tasks

Search for tasks by keyword.

```bash
python -m src.cli search <keyword>
```

**Arguments:**
- `<keyword>`: The keyword to search for in task titles and descriptions (required)

**Example:**
```bash
python -m src.cli search "documentation"
```

### View Task Details

View detailed information about a specific task.

```bash
python -m src.cli view <task-id>
```

**Arguments:**
- `<task-id>`: The ID of the task to view (required)

**Example:**
```bash
python -m src.cli view 1
```

## Output Format

The CLI provides formatted output for better readability:

- When listing tasks, the output is displayed in a table format with columns for ID, Title, Priority, Status, and Created At.
- When viewing a task, the output includes all task details in a readable format.
- When searching for tasks, the results are displayed in a table format similar to the list command.

## Error Handling

The CLI handles errors gracefully and provides informative error messages:

- If a task is not found, it displays "Error: Task with ID X not found"
- For other errors, it displays "An unexpected error occurred: [error message]"

## Examples

### Complete Workflow Example

```bash
# Add a new task
python -m src.cli add "Write documentation" -d "Create comprehensive documentation for the project" -p high

# List all active tasks
python -m src.cli list

# Mark the task as complete
python -m src.cli complete 1

# List all tasks including completed ones
python -m src.cli list -a

# Search for tasks containing "documentation"
python -m src.cli search "documentation"

# View details of a specific task
python -m src.cli view 1

# Delete the task
python -m src.cli delete 1
```