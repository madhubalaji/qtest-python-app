"""Tests for the Task model."""

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
        assert task.created_at is not None

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
        task = Task(3, "Dict Task", "Description", "low", True, "2023-01-01 12:00:00")
        task_dict = task.to_dict()
        
        expected = {
            "id": 3,
            "title": "Dict Task",
            "description": "Description",
            "priority": "low",
            "completed": True,
            "created_at": "2023-01-01 12:00:00"
        }
        
        assert task_dict == expected

    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        task_data = {
            "id": 4,
            "title": "From Dict Task",
            "description": "From dict description",
            "priority": "high",
            "completed": False,
            "created_at": "2023-01-01 15:30:00"
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 4
        assert task.title == "From Dict Task"
        assert task.description == "From dict description"
        assert task.priority == "high"
        assert task.completed is False
        assert task.created_at == "2023-01-01 15:30:00"

    def test_task_from_dict_with_defaults(self):
        """Test creating task from dictionary with missing optional fields."""
        task_data = {
            "id": 5,
            "title": "Minimal Task"
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 5
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert task.created_at is not None

    def test_task_str_representation(self):
        """Test string representation of task."""
        task = Task(6, "String Task", "Description", "medium", False)
        str_repr = str(task)
        
        assert "Task 6" in str_repr
        assert "String Task" in str_repr
        assert "Active" in str_repr
        assert "medium priority" in str_repr

    def test_completed_task_str_representation(self):
        """Test string representation of completed task."""
        task = Task(7, "Completed Task", "Description", "high", True)
        str_repr = str(task)
        
        assert "Task 7" in str_repr
        assert "Completed Task" in str_repr
        assert "Completed" in str_repr
        assert "high priority" in str_repr