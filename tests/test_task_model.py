"""
Tests for the Task model.
"""

import pytest
from datetime import datetime
from src.models.task import Task


class TestTask:
    """Test cases for the Task model."""

    def test_task_creation(self):
        """Test creating a new task with default values."""
        task = Task(1, "Test Task")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert task.created_at is not None

    def test_task_creation_with_all_parameters(self):
        """Test creating a task with all parameters specified."""
        created_at = "2023-01-01 12:00:00"
        task = Task(
            task_id=2,
            title="Important Task",
            description="This is important",
            priority="high",
            completed=True,
            created_at=created_at
        )
        
        assert task.id == 2
        assert task.title == "Important Task"
        assert task.description == "This is important"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == created_at

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(1, "Test Task", "Description", "low", True, "2023-01-01 12:00:00")
        task_dict = task.to_dict()
        
        expected = {
            "id": 1,
            "title": "Test Task",
            "description": "Description",
            "priority": "low",
            "completed": True,
            "created_at": "2023-01-01 12:00:00"
        }
        
        assert task_dict == expected

    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        task_data = {
            "id": 3,
            "title": "From Dict Task",
            "description": "Created from dict",
            "priority": "high",
            "completed": False,
            "created_at": "2023-01-01 12:00:00"
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 3
        assert task.title == "From Dict Task"
        assert task.description == "Created from dict"
        assert task.priority == "high"
        assert task.completed is False
        assert task.created_at == "2023-01-01 12:00:00"

    def test_task_from_dict_with_missing_optional_fields(self):
        """Test creating task from dictionary with missing optional fields."""
        task_data = {
            "id": 4,
            "title": "Minimal Task"
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 4
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert task.created_at is not None

    def test_task_string_representation(self):
        """Test string representation of task."""
        task = Task(1, "Test Task", priority="high", completed=False)
        expected = "Task 1: Test Task (Active, high priority)"
        assert str(task) == expected
        
        task.completed = True
        expected = "Task 1: Test Task (Completed, high priority)"
        assert str(task) == expected