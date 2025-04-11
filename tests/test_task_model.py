"""
Tests for the Task model.
"""

import unittest
import sys
import os
from datetime import datetime

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.task import Task


class TestTaskModel(unittest.TestCase):
    """Test cases for the Task model."""

    def test_task_creation(self):
        """Test creating a task."""
        task = Task(1, "Test Task", "This is a test task", "high")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.priority, "high")
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.created_at)

    def test_task_to_dict(self):
        """Test converting a task to a dictionary."""
        created_at = "2023-01-01 12:00:00"
        task = Task(1, "Test Task", "This is a test task", "high", False, created_at)
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict["id"], 1)
        self.assertEqual(task_dict["title"], "Test Task")
        self.assertEqual(task_dict["description"], "This is a test task")
        self.assertEqual(task_dict["priority"], "high")
        self.assertFalse(task_dict["completed"])
        self.assertEqual(task_dict["created_at"], created_at)

    def test_task_from_dict(self):
        """Test creating a task from a dictionary."""
        task_dict = {
            "id": 1,
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 12:00:00"
        }
        
        task = Task.from_dict(task_dict)
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.priority, "high")
        self.assertTrue(task.completed)
        self.assertEqual(task.created_at, "2023-01-01 12:00:00")

    def test_task_from_dict_with_defaults(self):
        """Test creating a task from a dictionary with default values."""
        task_dict = {
            "id": 1,
            "title": "Test Task"
        }
        
        task = Task.from_dict(task_dict)
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.completed)

    def test_task_string_representation(self):
        """Test the string representation of a task."""
        task = Task(1, "Test Task", "This is a test task", "high")
        self.assertEqual(str(task), "Task 1: Test Task (Active, high priority)")
        
        task.completed = True
        self.assertEqual(str(task), "Task 1: Test Task (Completed, high priority)")


if __name__ == "__main__":
    unittest.main()
