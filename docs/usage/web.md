# Web Interface Documentation

The Task Manager provides a user-friendly web interface built with Streamlit, allowing you to manage your tasks through a graphical user interface.

## Getting Started

To start the web interface, run:

```bash
streamlit run src/app.py
```

This will start the Streamlit server and open the web interface in your default web browser. If the browser doesn't open automatically, you can access the web interface by navigating to the URL displayed in the terminal (typically http://localhost:8501).

## Navigation

The web interface consists of three main pages, accessible through the sidebar navigation:

1. **View Tasks**: Display and manage your tasks
2. **Add Task**: Create new tasks
3. **Search Tasks**: Find tasks by keyword

## View Tasks Page

The View Tasks page displays your tasks and allows you to manage them.

### Features

- **Filter Options**:
  - **Show completed tasks**: Toggle to show or hide completed tasks
  - **Filter by priority**: Select a priority level (All, Low, Medium, High) to filter tasks

- **Task Display**:
  - Each task is displayed with its title, priority, and a completion button
  - Completed tasks are displayed with a strikethrough title
  - Click on "Details" to expand and view the task description and creation date
  - Click the checkmark (✓) button to mark a task as complete

### Example

1. Navigate to the "View Tasks" page using the sidebar
2. Toggle "Show completed tasks" to view all tasks
3. Select "High" from the priority filter to view only high-priority tasks
4. Click on "Details" under a task to view its description
5. Click the checkmark button to mark a task as complete

## Add Task Page

The Add Task page allows you to create new tasks.

### Features

- **Task Form**:
  - **Title**: Enter the task title (required, max 50 characters)
  - **Description**: Enter a detailed description of the task (optional, max 200 characters)
  - **Priority**: Select the task priority using a slider (Low, Medium, High)
  - **Add Task Button**: Submit the form to create a new task

### Example

1. Navigate to the "Add Task" page using the sidebar
2. Enter "Complete project documentation" in the Title field
3. Enter "Write comprehensive documentation for the project" in the Description field
4. Set the Priority slider to "High"
5. Click the "Add Task" button
6. A success message will appear confirming that the task has been added

## Search Tasks Page

The Search Tasks page allows you to find tasks by keyword.

### Features

- **Search Box**: Enter a keyword to search for in task titles and descriptions
- **Search Results**:
  - Displays tasks matching the search keyword
  - Shows the task title, status, and priority
  - Click on "Details" to expand and view the task description and creation date
  - Click the "View" button to see full task details

### Task Details View

When you click the "View" button on a search result, a detailed view of the task appears:

- **Task Information**:
  - ID
  - Title
  - Description
  - Priority
  - Status
  - Creation date
- **Action Buttons**:
  - **Mark as Complete**: Available for active tasks
  - **Close**: Close the detailed view

### Example

1. Navigate to the "Search Tasks" page using the sidebar
2. Enter "documentation" in the search box
3. View the list of tasks matching the keyword
4. Click on "Details" under a task to view its description
5. Click the "View" button to see full task details
6. If the task is active, click "Mark as Complete" to complete it
7. Click "Close" to return to the search results

## Responsive Design

The web interface is designed to be responsive and works well on both desktop and mobile devices. The layout adjusts automatically based on the screen size.

## Error Handling

The web interface handles errors gracefully and provides informative error messages:

- If a required field is missing, an error message is displayed
- If a task is not found, an error message is displayed
- Success messages are displayed when actions are completed successfully