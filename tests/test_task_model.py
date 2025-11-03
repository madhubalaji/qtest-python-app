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
        task = Task(1, "Test Task", "Test description", "high", False)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.priority == "high"
        assert task.completed is False
        assert task.created_at is not None

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(1, "Test Task")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert task.created_at is not None

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(1, "Test Task", "Test description", "high", True, "2023-01-01 12:00:00")
        task_dict = task.to_dict()
        
        expected = {
            "id": 1,
            "title": "Test Task",
            "description": "Test description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 12:00:00"
        }
        
        assert task_dict == expected

    def test_task_from_dict_complete(self):
        """Test creating task from complete dictionary."""
        task_dict = {
            "id": 1,
            "title": "Test Task",
            "description": "Test description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 12:00:00"
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == "2023-01-01 12:00:00"

    def test_task_from_dict_minimal(self):
        """Test creating task from minimal dictionary."""
        task_dict = {
            "id": 1,
            "title": "Test Task"
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        # When created_at is not provided, it should be auto-generated
        assert task.created_at is not None
        assert isinstance(task.created_at, str)

    def test_task_from_dict_partial(self):
        """Test creating task from partial dictionary."""
        task_dict = {
            "id": 1,
            "title": "Test Task",
            "priority": "low",
            "completed": True
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "low"
        assert task.completed is True
        # When created_at is not provided, it should be auto-generated
        assert task.created_at is not None
        assert isinstance(task.created_at, str)

    def test_task_from_dict_with_none_created_at(self):
        """Test creating task from dictionary with None created_at."""
        task_dict = {
            "id": 1,
            "title": "Test Task",
            "created_at": None
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 1
        assert task.title == "Test Task"
        # When created_at is None, it should be auto-generated
        assert task.created_at is not None
        assert isinstance(task.created_at, str)

    def test_task_str_representation(self):
        """Test string representation of task."""
        task = Task(1, "Test Task", "Test description", "high", False)
        expected = "Task 1: Test Task (Active, high priority)"
        assert str(task) == expected

    def test_task_str_representation_completed(self):
        """Test string representation of completed task."""
        task = Task(1, "Test Task", "Test description", "high", True)
        expected = "Task 1: Test Task (Completed, high priority)"
        assert str(task) == expected

    def test_task_created_at_format(self):
        """Test that created_at is in the correct format."""
        task = Task(1, "Test Task")
        # Should be in format YYYY-MM-DD HH:MM:SS
        assert len(task.created_at) == 19
        assert task.created_at[4] == '-'
        assert task.created_at[7] == '-'
        assert task.created_at[10] == ' '
        assert task.created_at[13] == ':'
        assert task.created_at[16] == ':'