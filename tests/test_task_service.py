"""
Unit tests for TaskService class.
"""

import os
import tempfile
import unittest
from unittest.mock import patch

from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService(unittest.TestCase):
    """Test cases for TaskService class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.task_service = TaskService(self.temp_file.name)

    def tearDown(self):
        """Clean up after each test method."""
        # Remove the temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_delete_task_success(self):
        """Test successful task deletion."""
        # Add a task first
        task = self.task_service.add_task("Test Task", "Test Description", "high")
        task_id = task.id
        
        # Verify task exists
        self.assertEqual(len(self.task_service.tasks), 1)
        
        # Delete the task
        deleted_task = self.task_service.delete_task(task_id)
        
        # Verify task was deleted
        self.assertEqual(deleted_task.id, task_id)
        self.assertEqual(deleted_task.title, "Test Task")
        self.assertEqual(len(self.task_service.tasks), 0)

    def test_delete_task_not_found(self):
        """Test deletion of non-existent task."""
        # Try to delete a task that doesn't exist
        with self.assertRaises(TaskNotFoundException):
            self.task_service.delete_task(999)

    def test_delete_task_from_multiple_tasks(self):
        """Test deleting a specific task when multiple tasks exist."""
        # Add multiple tasks
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        task3 = self.task_service.add_task("Task 3", "Description 3", "high")
        
        # Verify all tasks exist
        self.assertEqual(len(self.task_service.tasks), 3)
        
        # Delete the middle task
        deleted_task = self.task_service.delete_task(task2.id)
        
        # Verify correct task was deleted
        self.assertEqual(deleted_task.id, task2.id)
        self.assertEqual(deleted_task.title, "Task 2")
        self.assertEqual(len(self.task_service.tasks), 2)
        
        # Verify remaining tasks are correct
        remaining_ids = [task.id for task in self.task_service.tasks]
        self.assertIn(task1.id, remaining_ids)
        self.assertIn(task3.id, remaining_ids)
        self.assertNotIn(task2.id, remaining_ids)

    def test_delete_completed_task(self):
        """Test deleting a completed task."""
        # Add and complete a task
        task = self.task_service.add_task("Completed Task", "Test Description", "medium")
        self.task_service.complete_task(task.id)
        
        # Verify task is completed
        completed_task = self.task_service.get_task_by_id(task.id)
        self.assertTrue(completed_task.completed)
        
        # Delete the completed task
        deleted_task = self.task_service.delete_task(task.id)
        
        # Verify task was deleted
        self.assertEqual(deleted_task.id, task.id)
        self.assertTrue(deleted_task.completed)
        self.assertEqual(len(self.task_service.tasks), 0)

    def test_delete_task_persistence(self):
        """Test that task deletion is persisted to storage."""
        # Add a task
        task = self.task_service.add_task("Persistent Task", "Test Description", "low")
        task_id = task.id
        
        # Create a new service instance with the same file
        new_service = TaskService(self.temp_file.name)
        self.assertEqual(len(new_service.tasks), 1)
        
        # Delete the task using the new service
        new_service.delete_task(task_id)
        
        # Create another service instance to verify persistence
        another_service = TaskService(self.temp_file.name)
        self.assertEqual(len(another_service.tasks), 0)

    def test_delete_task_after_get_by_id(self):
        """Test deleting a task after retrieving it by ID."""
        # Add a task
        task = self.task_service.add_task("Get and Delete", "Test Description", "high")
        task_id = task.id
        
        # Get the task by ID
        retrieved_task = self.task_service.get_task_by_id(task_id)
        self.assertEqual(retrieved_task.id, task_id)
        
        # Delete the task
        deleted_task = self.task_service.delete_task(task_id)
        self.assertEqual(deleted_task.id, task_id)
        
        # Verify task no longer exists
        with self.assertRaises(TaskNotFoundException):
            self.task_service.get_task_by_id(task_id)


if __name__ == '__main__':
    unittest.main()