"""
Tests for the TaskService class.
"""

import unittest
import sys
import os
import tempfile
import json

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService(unittest.TestCase):
    """Test cases for the TaskService class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for task storage
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.task_service = TaskService(self.temp_file.name)

    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary file
        os.unlink(self.temp_file.name)

    def test_add_task(self):
        """Test adding a task."""
        task = self.task_service.add_task("Test Task", "This is a test task", "high")
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.priority, "high")
        self.assertFalse(task.completed)
        
        # Check that the task was saved to the file
        with open(self.temp_file.name, "r") as f:
            saved_tasks = json.load(f)
            self.assertEqual(len(saved_tasks), 1)
            self.assertEqual(saved_tasks[0]["id"], 1)
            self.assertEqual(saved_tasks[0]["title"], "Test Task")

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        # Add some tasks
        self.task_service.add_task("Task 1", "Description 1", "low")
        self.task_service.add_task("Task 2", "Description 2", "medium")
        task3 = self.task_service.add_task("Task 3", "Description 3", "high")
        
        # Mark one task as completed
        task3.completed = True
        self.task_service._save_tasks()
        
        # Get all tasks
        all_tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(all_tasks), 3)
        
        # Get only active tasks
        active_tasks = self.task_service.get_all_tasks(show_completed=False)
        self.assertEqual(len(active_tasks), 2)
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
        
        # Try to get a non-existent task
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
            priority="high"
        )
        
        self.assertEqual(updated_task.id, task.id)
        self.assertEqual(updated_task.title, "Updated Title")
        self.assertEqual(updated_task.description, "Updated Description")
        self.assertEqual(updated_task.priority, "high")
        
        # Check that the task was updated in the file
        with open(self.temp_file.name, "r") as f:
            saved_tasks = json.load(f)
            self.assertEqual(saved_tasks[0]["title"], "Updated Title")

    def test_complete_task(self):
        """Test marking a task as complete."""
        # Add a task
        task = self.task_service.add_task("Test Task")
        self.assertFalse(task.completed)
        
        # Mark the task as complete
        completed_task = self.task_service.complete_task(task.id)
        self.assertTrue(completed_task.completed)
        
        # Check that the task was updated in the file
        with open(self.temp_file.name, "r") as f:
            saved_tasks = json.load(f)
            self.assertTrue(saved_tasks[0]["completed"])

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
        
        # Check that the task was deleted
        tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 3)
        
        # Try to delete a non-existent task
        with self.assertRaises(TaskNotFoundException):
            self.task_service.delete_task(2)

    def test_search_tasks(self):
        """Test searching for tasks."""
        # Add some tasks
        self.task_service.add_task("Meeting with client", "Discuss project requirements")
        self.task_service.add_task("Buy groceries", "Milk, eggs, bread")
        self.task_service.add_task("Project planning", "Plan the next sprint")
        
        # Search for tasks
        results = self.task_service.search_tasks("project")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, "Meeting with client")
        self.assertEqual(results[1].title, "Project planning")
        
        # Search for a non-existent keyword
        results = self.task_service.search_tasks("nonexistent")
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
