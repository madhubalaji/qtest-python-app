"""
Tests for the TaskService class.
"""

import unittest
import os
import json
import tempfile
from unittest.mock import patch, mock_open
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService(unittest.TestCase):
    """Test cases for the TaskService class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False).name
        self.task_service = TaskService(self.temp_file)

    def tearDown(self):
        """Clean up after tests."""
        # Remove the temporary file
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_add_task(self):
        """Test adding a task."""
        task = self.task_service.add_task("Test Task", "Description", "high")
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Description")
        self.assertEqual(task.priority, "high")
        self.assertFalse(task.completed)
        
        # Check that the task was added to the list
        self.assertEqual(len(self.task_service.tasks), 1)
        self.assertEqual(self.task_service.tasks[0].id, 1)
        self.assertEqual(self.task_service.tasks[0].title, "Test Task")

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks."""
        task1 = self.task_service.add_task("Task 1")
        task2 = self.task_service.add_task("Task 2")
        task3 = self.task_service.add_task("Task 3")
        
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)
        
        self.assertEqual(len(self.task_service.tasks), 3)

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        # Add some tasks
        self.task_service.add_task("Task 1")
        self.task_service.add_task("Task 2")
        self.task_service.add_task("Task 3", completed=True)
        
        # Get all tasks
        all_tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(all_tasks), 3)
        
        # Get only active tasks
        active_tasks = self.task_service.get_all_tasks(show_completed=False)
        self.assertEqual(len(active_tasks), 2)
        
        # Check that the active tasks are the ones we expect
        self.assertEqual(active_tasks[0].title, "Task 1")
        self.assertEqual(active_tasks[1].title, "Task 2")

    def test_get_task_by_id(self):
        """Test getting a task by ID."""
        # Add some tasks
        self.task_service.add_task("Task 1")
        self.task_service.add_task("Task 2")
        
        # Get task by ID
        task = self.task_service.get_task_by_id(2)
        self.assertEqual(task.id, 2)
        self.assertEqual(task.title, "Task 2")
        
        # Test getting a non-existent task
        with self.assertRaises(TaskNotFoundException):
            self.task_service.get_task_by_id(999)

    def test_update_task(self):
        """Test updating a task."""
        # Add a task
        task = self.task_service.add_task("Original Title", "Original Description", "low")
        
        # Update the task
        updated_task = self.task_service.update_task(
            task.id,
            title="Updated Title",
            description="Updated Description",
            priority="high",
            completed=True
        )
        
        # Check that the task was updated
        self.assertEqual(updated_task.title, "Updated Title")
        self.assertEqual(updated_task.description, "Updated Description")
        self.assertEqual(updated_task.priority, "high")
        self.assertTrue(updated_task.completed)
        
        # Check that the task in the list was updated
        task_in_list = self.task_service.get_task_by_id(task.id)
        self.assertEqual(task_in_list.title, "Updated Title")
        
        # Test updating a non-existent task
        with self.assertRaises(TaskNotFoundException):
            self.task_service.update_task(999, title="Non-existent")

    def test_complete_task(self):
        """Test marking a task as complete."""
        # Add a task
        task = self.task_service.add_task("Test Task")
        self.assertFalse(task.completed)
        
        # Complete the task
        completed_task = self.task_service.complete_task(task.id)
        self.assertTrue(completed_task.completed)
        
        # Check that the task in the list was updated
        task_in_list = self.task_service.get_task_by_id(task.id)
        self.assertTrue(task_in_list.completed)
        
        # Test completing a non-existent task
        with self.assertRaises(TaskNotFoundException):
            self.task_service.complete_task(999)

    def test_delete_task(self):
        """Test deleting a task."""
        # Add some tasks
        self.task_service.add_task("Task 1")
        self.task_service.add_task("Task 2")
        self.task_service.add_task("Task 3")
        
        # Delete a task
        deleted_task = self.task_service.delete_task(2)
        self.assertEqual(deleted_task.id, 2)
        self.assertEqual(deleted_task.title, "Task 2")
        
        # Check that the task was removed from the list
        self.assertEqual(len(self.task_service.tasks), 2)
        self.assertEqual(self.task_service.tasks[0].id, 1)
        self.assertEqual(self.task_service.tasks[1].id, 3)
        
        # Test deleting a non-existent task
        with self.assertRaises(TaskNotFoundException):
            self.task_service.delete_task(2)  # Already deleted

    def test_search_tasks(self):
        """Test searching for tasks."""
        # Add some tasks
        self.task_service.add_task("Apple Task", "This is about apples")
        self.task_service.add_task("Banana Task", "This is about bananas")
        self.task_service.add_task("Cherry Task", "This is about cherries")
        self.task_service.add_task("Apple Pie", "Recipe for apple pie")
        
        # Search for tasks containing "apple"
        results = self.task_service.search_tasks("apple")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, "Apple Task")
        self.assertEqual(results[1].title, "Apple Pie")
        
        # Search for tasks containing "banana"
        results = self.task_service.search_tasks("banana")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Banana Task")
        
        # Search for tasks containing "fruit" (should return none)
        results = self.task_service.search_tasks("fruit")
        self.assertEqual(len(results), 0)
        
        # Test case insensitivity
        results = self.task_service.search_tasks("APPLE")
        self.assertEqual(len(results), 2)

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "title": "Mocked Task", "description": "Mocked Description", "priority": "high", "completed": false, "created_at": "2023-01-01 12:00:00"}]')
    def test_load_tasks(self, mock_file, mock_exists):
        """Test loading tasks from a file."""
        mock_exists.return_value = True
        
        # Create a new TaskService to trigger _load_tasks
        task_service = TaskService("mocked_file.json")
        
        # Check that the tasks were loaded correctly
        self.assertEqual(len(task_service.tasks), 1)
        self.assertEqual(task_service.tasks[0].id, 1)
        self.assertEqual(task_service.tasks[0].title, "Mocked Task")
        self.assertEqual(task_service.tasks[0].description, "Mocked Description")
        self.assertEqual(task_service.tasks[0].priority, "high")
        self.assertFalse(task_service.tasks[0].completed)
        self.assertEqual(task_service.tasks[0].created_at, "2023-01-01 12:00:00")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_tasks(self, mock_file):
        """Test saving tasks to a file."""
        # Add a task
        self.task_service.add_task("Test Task", "Test Description", "high")
        
        # Check that the file was opened for writing
        mock_file.assert_called_with(self.temp_file, "w")
        
        # Check that json.dump was called with the correct data
        handle = mock_file()
        handle.write.assert_called()  # json.dump writes to the file

    @patch("os.path.exists")
    @patch("builtins.open", side_effect=json.JSONDecodeError("Expecting value", "", 0))
    def test_load_tasks_with_invalid_json(self, mock_file, mock_exists):
        """Test loading tasks from a file with invalid JSON."""
        mock_exists.return_value = True
        
        # Create a new TaskService to trigger _load_tasks
        task_service = TaskService("invalid_file.json")
        
        # Check that an empty task list was created
        self.assertEqual(len(task_service.tasks), 0)


if __name__ == "__main__":
    unittest.main()