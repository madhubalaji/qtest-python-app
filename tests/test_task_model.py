"""
Tests for the Task model.
"""

import pytest
from datetime import datetime

from src.models.task import Task


class TestTask:
    """Test class for Task model."""

    def test_task_creation(self):
        """Test creating a new task."""
        task = Task(1, "Test Task", "Test Description", "high")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed is False
        assert isinstance(task.created_at, str)  # Changed from datetime to str

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(2, "Another Task")

        assert task.id == 2
        assert task.title == "Another Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert isinstance(task.created_at, str)

    def test_task_creation_with_custom_created_at(self):
        """Test creating a task with custom created_at."""
        custom_time = "2023-01-01 12:00:00"
        task = Task(3, "Custom Time Task", created_at=custom_time)

        assert task.created_at == custom_time

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(1, "Test Task", "Test Description", "high", True, "2023-01-01 10:00:00")
        task_dict = task.to_dict()

        expected_dict = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 10:00:00"
        }

        assert task_dict == expected_dict

    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        task_data = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 10:00:00"
        }

        task = Task.from_dict(task_data)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == "2023-01-01 10:00:00"

    def test_task_from_dict_with_defaults(self):
        """Test creating task from dictionary with missing optional fields."""
        task_data = {
            "id": 2,
            "title": "Minimal Task"
        }

        task = Task.from_dict(task_data)

        assert task.id == 2
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert isinstance(task.created_at, str)

    def test_task_str_representation(self):
        """Test string representation of task."""
        task = Task(1, "Test Task", "Test Description", "high", False)
        str_repr = str(task)

        assert "Task 1: Test Task" in str_repr
        assert "Active" in str_repr
        assert "high priority" in str_repr

    def test_completed_task_str_representation(self):
        """Test string representation of completed task."""
        task = Task(1, "Test Task", "Test Description", "high", True)
        str_repr = str(task)

        assert "Task 1: Test Task" in str_repr
        assert "Completed" in str_repr
        assert "high priority" in str_repr