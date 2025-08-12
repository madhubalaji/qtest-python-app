"""
Tests for the Task model.
"""

import pytest
from datetime import datetime
from src.models.task import Task


class TestTask:
    """Test cases for the Task model."""

    def test_task_creation(self):
        """Test creating a new task."""
        task = Task(1, "Test Task", "Test Description", "high")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed is False
        assert isinstance(task.created_at, datetime)

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(2, "Another Task")
        
        assert task.id == 2
        assert task.title == "Another Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(3, "Dict Task", "Description", "low")
        task_dict = task.to_dict()
        
        expected_keys = {"id", "title", "description", "priority", "completed", "created_at"}
        assert set(task_dict.keys()) == expected_keys
        assert task_dict["id"] == 3
        assert task_dict["title"] == "Dict Task"
        assert task_dict["description"] == "Description"
        assert task_dict["priority"] == "low"
        assert task_dict["completed"] is False

    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        task_dict = {
            "id": 4,
            "title": "From Dict Task",
            "description": "From dict description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01T12:00:00"
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 4
        assert task.title == "From Dict Task"
        assert task.description == "From dict description"
        assert task.priority == "high"
        assert task.completed is True

    def test_task_str_representation(self):
        """Test string representation of task."""
        task = Task(5, "String Task", "String description", "medium")
        task_str = str(task)
        
        assert "String Task" in task_str
        assert "medium" in task_str
        assert "Active" in task_str

    def test_completed_task_str_representation(self):
        """Test string representation of completed task."""
        task = Task(6, "Completed Task", "Completed description", "low")
        task.completed = True
        task_str = str(task)
        
        assert "Completed Task" in task_str
        assert "low" in task_str
        assert "Completed" in task_str

    def test_task_equality(self):
        """Test task equality comparison."""
        task1 = Task(7, "Equal Task", "Description", "high")
        task2 = Task(7, "Equal Task", "Description", "high")
        task3 = Task(8, "Different Task", "Description", "high")
        
        assert task1 == task2
        assert task1 != task3

    def test_task_hash(self):
        """Test task hashing."""
        task1 = Task(9, "Hash Task", "Description", "medium")
        task2 = Task(9, "Hash Task", "Description", "medium")
        
        assert hash(task1) == hash(task2)
        
        # Test that tasks can be used in sets
        task_set = {task1, task2}
        assert len(task_set) == 1

    def test_task_completion_toggle(self):
        """Test toggling task completion status."""
        task = Task(10, "Toggle Task", "Description", "low")
        
        assert task.completed is False
        
        task.completed = True
        assert task.completed is True
        
        task.completed = False
        assert task.completed is False