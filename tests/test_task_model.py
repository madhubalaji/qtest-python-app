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
        # Test with minimal parameters
        task = Task(task_id=1, title="Test Task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.created_at)

        # Test with all parameters
        created_at = "2023-01-01 12:00:00"
        task = Task(
            task_id=2,
            title="Complete Task",
            description="This is a test task",
            priority="high",
            completed=True,
            created_at=created_at
        )
        self.assertEqual(task.id, 2)
        self.assertEqual(task.title, "Complete Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.priority, "high")
        self.assertTrue(task.completed)
        self.assertEqual(task.created_at, created_at)

    def test_to_dict(self):
        """Test that to_dict returns the correct dictionary representation."""
        created_at = "2023-01-01 12:00:00"
        task = Task(
            task_id=1,
            title="Test Task",
            description="Description",
            priority="low",
            completed=False,
            created_at=created_at
        )
        
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict["id"], 1)
        self.assertEqual(task_dict["title"], "Test Task")
        self.assertEqual(task_dict["description"], "Description")
        self.assertEqual(task_dict["priority"], "low")
        self.assertFalse(task_dict["completed"])
        self.assertEqual(task_dict["created_at"], created_at)

    def test_from_dict(self):
        """Test that from_dict creates a Task with the correct attributes."""
        task_dict = {
            "id": 3,
            "title": "Dict Task",
            "description": "Created from dict",
            "priority": "high",
            "completed": True,
            "created_at": "2023-02-01 15:30:00"
        }
        
        task = Task.from_dict(task_dict)
        
        self.assertEqual(task.id, 3)
        self.assertEqual(task.title, "Dict Task")
        self.assertEqual(task.description, "Created from dict")
        self.assertEqual(task.priority, "high")
        self.assertTrue(task.completed)
        self.assertEqual(task.created_at, "2023-02-01 15:30:00")

    def test_from_dict_with_minimal_data(self):
        """Test that from_dict works with minimal data."""
        task_dict = {
            "id": 4,
            "title": "Minimal Task"
        }
        
        task = Task.from_dict(task_dict)
        
        self.assertEqual(task.id, 4)
        self.assertEqual(task.title, "Minimal Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.completed)
        self.assertIsNone(task.created_at)

    def test_str_representation(self):
        """Test the string representation of a Task."""
        # Test active task
        task = Task(task_id=1, title="Active Task")
        self.assertEqual(str(task), "Task 1: Active Task (Active, medium priority)")
        
        # Test completed task
        task = Task(task_id=2, title="Completed Task", completed=True)
        self.assertEqual(str(task), "Task 2: Completed Task (Completed, medium priority)")
        
        # Test with different priority
        task = Task(task_id=3, title="High Priority", priority="high")
        self.assertEqual(str(task), "Task 3: High Priority (Active, high priority)")


if __name__ == "__main__":
    unittest.main()