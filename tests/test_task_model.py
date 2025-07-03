"""
Tests for the Task model.
"""

import unittest
from datetime import datetime

from src.models.task import Task


class TestTaskModel(unittest.TestCase):
    """Test cases for the Task model."""

    def test_task_initialization(self):
        """Test task initialization with default values."""
        task = Task(1, "Test Task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.completed)
        # Check that created_at is a valid datetime string
        datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")

    def test_task_initialization_with_values(self):
        """Test task initialization with custom values."""
        task = Task(
            2, 
            "Custom Task", 
            "Custom Description", 
            "high", 
            True, 
            "2023-01-01 12:00:00"
        )
        self.assertEqual(task.id, 2)
        self.assertEqual(task.title, "Custom Task")
        self.assertEqual(task.description, "Custom Description")
        self.assertEqual(task.priority, "high")
        self.assertTrue(task.completed)
        self.assertEqual(task.created_at, "2023-01-01 12:00:00")

    def test_to_dict(self):
        """Test converting a task to a dictionary."""
        task = Task(
            3, 
            "Dict Task", 
            "Dict Description", 
            "low", 
            False, 
            "2023-02-01 12:00:00"
        )
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict["id"], 3)
        self.assertEqual(task_dict["title"], "Dict Task")
        self.assertEqual(task_dict["description"], "Dict Description")
        self.assertEqual(task_dict["priority"], "low")
        self.assertFalse(task_dict["completed"])
        self.assertEqual(task_dict["created_at"], "2023-02-01 12:00:00")

    def test_from_dict(self):
        """Test creating a task from a dictionary."""
        task_dict = {
            "id": 4,
            "title": "From Dict Task",
            "description": "From Dict Description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-03-01 12:00:00"
        }
        
        task = Task.from_dict(task_dict)
        
        self.assertEqual(task.id, 4)
        self.assertEqual(task.title, "From Dict Task")
        self.assertEqual(task.description, "From Dict Description")
        self.assertEqual(task.priority, "high")
        self.assertTrue(task.completed)
        self.assertEqual(task.created_at, "2023-03-01 12:00:00")

    def test_from_dict_with_defaults(self):
        """Test creating a task from a dictionary with missing fields."""
        task_dict = {
            "id": 5,
            "title": "Minimal Task"
        }
        
        task = Task.from_dict(task_dict)
        
        self.assertEqual(task.id, 5)
        self.assertEqual(task.title, "Minimal Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.completed)

    def test_str_representation(self):
        """Test the string representation of a task."""
        task = Task(6, "String Task", priority="high")
        expected_str = "Task 6: String Task (Active, high priority)"
        self.assertEqual(str(task), expected_str)
        
        task.completed = True
        expected_str = "Task 6: String Task (Completed, high priority)"
        self.assertEqual(str(task), expected_str)


if __name__ == "__main__":
    unittest.main()