"""
Tests for the Task model.
"""

import unittest
from datetime import datetime
from src.models.task import Task


class TestTaskModel(unittest.TestCase):
    """Test cases for the Task model."""

    def test_task_initialization(self):
        """Test that a Task can be initialized with the correct attributes."""
        task = Task(1, "Test Task", "This is a test task", "high")
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.priority, "high")
        self.assertFalse(task.completed)
        # Check that created_at is a valid datetime string
        datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")

    def test_task_initialization_with_defaults(self):
        """Test that a Task can be initialized with default values."""
        task = Task(1, "Test Task")
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.completed)

    def test_task_to_dict(self):
        """Test that a Task can be converted to a dictionary."""
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
        """Test that a Task can be created from a dictionary."""
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
        """Test that a Task can be created from a dictionary with minimal fields."""
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

    def test_task_str_representation(self):
        """Test the string representation of a Task."""
        task = Task(1, "Test Task", "This is a test task", "high")
        expected_str = "Task 1: Test Task (Active, high priority)"
        self.assertEqual(str(task), expected_str)
        
        task.completed = True
        expected_str = "Task 1: Test Task (Completed, high priority)"
        self.assertEqual(str(task), expected_str)


if __name__ == "__main__":
    unittest.main()