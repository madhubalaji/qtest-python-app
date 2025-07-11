# Testing the Delete Task Functionality

This document outlines the manual testing procedures for the delete task functionality in the Task Manager web interface.

## Test Cases

### Test Case 1: Delete Task from View Tasks Page
1. **Setup**: Create a new task using the "Add Task" page
2. **Action**: Navigate to "View Tasks" page and click the delete button (🗑️) for the created task
3. **Expected Result**: A warning message appears asking for confirmation
4. **Action**: Click the delete button again
5. **Expected Result**: Task is deleted, success message appears, and task is no longer visible in the list

### Test Case 2: Cancel Delete Operation in View Tasks Page
1. **Setup**: Create a new task using the "Add Task" page
2. **Action**: Navigate to "View Tasks" page and click the delete button (🗑️) for the created task
3. **Expected Result**: A warning message appears asking for confirmation
4. **Action**: Navigate away from the page or refresh the page
5. **Expected Result**: Task is not deleted and still visible after returning to the page

### Test Case 3: Delete Task from Search Tasks Page
1. **Setup**: Create a new task with a unique keyword in the title
2. **Action**: Navigate to "Search Tasks" page and search for the unique keyword
3. **Action**: Click "View" button on the found task
4. **Action**: Click "Delete Task" button in the task details view
5. **Expected Result**: A warning message appears asking for confirmation
6. **Action**: Click "Delete Task" button again
7. **Expected Result**: Task is deleted, success message appears, and task details view is closed

### Test Case 4: Cancel Delete Operation in Search Tasks Page
1. **Setup**: Create a new task with a unique keyword in the title
2. **Action**: Navigate to "Search Tasks" page and search for the unique keyword
3. **Action**: Click "View" button on the found task
4. **Action**: Click "Delete Task" button in the task details view
5. **Expected Result**: A warning message appears asking for confirmation
6. **Action**: Click "Close" button instead of confirming deletion
7. **Expected Result**: Task is not deleted and still visible when searched again

### Test Case 5: Error Handling for Non-existent Task
1. **Setup**: Create a task and note its ID
2. **Action**: Delete the task using the CLI: `python -m src.cli delete <task-id>`
3. **Action**: Try to delete the same task from the web interface
4. **Expected Result**: Appropriate error handling should occur (no crashes)

## Test Results

| Test Case | Result | Notes |
|-----------|--------|-------|
| Test Case 1 | Pass | Task was successfully deleted after confirmation |
| Test Case 2 | Pass | Task remained after navigating away without confirming |
| Test Case 3 | Pass | Task was successfully deleted from search results view |
| Test Case 4 | Pass | Task remained after clicking Close instead of confirming |
| Test Case 5 | Pass | No crashes when attempting to delete non-existent task |

## Summary

The delete task functionality works as expected in both the "View Tasks" and "Search Tasks" pages. The confirmation mechanism successfully prevents accidental deletions, and the application handles error cases gracefully.