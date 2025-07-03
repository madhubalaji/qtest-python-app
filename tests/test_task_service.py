"""
Tests for the TaskService class.
"""

import os
import json
import tempfile
import unittest

from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService(unittest.TestCase):
    """Test cases for the TaskService class."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary file for task storage
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.task_service = TaskService(self.temp_file.name)

    def tearDown(self):
        """Clean up after each test."""
        os.unlink(self.temp_file.name)

    def test_add_task(self):
        """Test adding a task."""
        task = self.task_service.add_task("Test Task", "Test Description", "high")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.priority, "high")
        self.assertFalse(task.completed)
        self.assertEqual(len(self.task_service.tasks), 1)

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        self.task_service.add_task("Task 1")
        self.task_service.add_task("Task 2")
        tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(tasks), 2)

    def test_get_task_by_id(self):
        """Test getting a task by ID."""
        task = self.task_service.add_task("Test Task")
        retrieved_task = self.task_service.get_task_by_id(task.id)
        self.assertEqual(retrieved_task.id, task.id)
        self.assertEqual(retrieved_task.title, task.title)

    def test_get_task_by_id_not_found(self):
        """Test getting a non-existent task by ID."""
        with self.assertRaises(TaskNotFoundException):
            self.task_service.get_task_by_id(999)

    def test_update_task(self):
        """Test updating a task."""
        task = self.task_service.add_task("Test Task")
        updated_task = self.task_service.update_task(
            task.id, title="Updated Task", priority="high"
        )
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.priority, "high")

    def test_complete_task(self):
        """Test marking a task as complete."""
        task = self.task_service.add_task("Test Task")
        completed_task = self.task_service.complete_task(task.id)
        self.assertTrue(completed_task.completed)

    def test_delete_task(self):
        """Test deleting a task."""
        task = self.task_service.add_task("Test Task")
        self.assertEqual(len(self.task_service.tasks), 1)
        
        deleted_task = self.task_service.delete_task(task.id)
        self.assertEqual(deleted_task.id, task.id)
        self.assertEqual(len(self.task_service.tasks), 0)
        
        # Verify the task is actually removed from storage
        with open(self.temp_file.name, "r") as f:
            stored_tasks = json.load(f)
        self.assertEqual(len(stored_tasks), 0)

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        with self.assertRaises(TaskNotFoundException):
            self.task_service.delete_task(999)

    def test_search_tasks(self):
        """Test searching for tasks."""
        self.task_service.add_task("Task One", "First task")
        self.task_service.add_task("Task Two", "Second task")
        self.task_service.add_task("Another Task", "Third task")
        
        results = self.task_service.search_tasks("Task")
        self.assertEqual(len(results), 3)
        
        results = self.task_service.search_tasks("One")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task One")


if __name__ == "__main__":
    unittest.main()