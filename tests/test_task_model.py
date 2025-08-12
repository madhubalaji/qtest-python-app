"""
Tests for the Task model.
"""

import pytest
from datetime import datetime
from src.models.task import Task


class TestTask:
    """Test cases for the Task model."""

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields provided."""
        task = Task(
            task_id=1,
            title="Test Task",
            description="Test Description",
            priority="high",
            completed=True,
            created_at="2023-01-01 12:00:00"
        )
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == "2023-01-01 12:00:00"

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(task_id=2, title="Default Task")
        
        assert task.id == 2
        assert task.title == "Default Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert task.created_at is not None
        assert isinstance(task.created_at, str)

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            task_id=3,
            title="Dict Task",
            description="Dict Description",
            priority="low",
            completed=False,
            created_at="2023-01-01 10:00:00"
        )
        
        expected_dict = {
            "id": 3,
            "title": "Dict Task",
            "description": "Dict Description",
            "priority": "low",
            "completed": False,
            "created_at": "2023-01-01 10:00:00"
        }
        
        assert task.to_dict() == expected_dict

    def test_task_from_dict_with_all_fields(self):
        """Test creating task from dictionary with all fields."""
        task_dict = {
            "id": 4,
            "title": "From Dict Task",
            "description": "From Dict Description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 14:00:00"
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 4
        assert task.title == "From Dict Task"
        assert task.description == "From Dict Description"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == "2023-01-01 14:00:00"

    def test_task_from_dict_with_missing_optional_fields(self):
        """Test creating task from dictionary with missing optional fields."""
        task_dict = {
            "id": 5,
            "title": "Minimal Task"
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 5
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        # When created_at is not provided, it should get a timestamp
        assert task.created_at is not None
        assert isinstance(task.created_at, str)

    def test_task_from_dict_with_explicit_none_created_at(self):
        """Test creating task from dictionary with explicit None created_at."""
        task_dict = {
            "id": 6,
            "title": "None Created At Task",
            "created_at": None
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 6
        assert task.title == "None Created At Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        # When created_at is explicitly None, it should get a timestamp
        assert task.created_at is not None
        assert isinstance(task.created_at, str)

    def test_task_str_representation(self):
        """Test string representation of task."""
        task = Task(task_id=7, title="String Task", priority="high", completed=False)
        expected_str = "Task 7: String Task (Active, high priority)"
        assert str(task) == expected_str
        
        completed_task = Task(task_id=8, title="Completed Task", completed=True)
        expected_str_completed = "Task 8: Completed Task (Completed, medium priority)"
        assert str(completed_task) == expected_str_completed

    def test_task_validation_required_fields(self):
        """Test that required fields are properly handled."""
        # Test that task_id and title are required
        with pytest.raises(TypeError):
            Task()
        
        with pytest.raises(TypeError):
            Task(task_id=1)

    def test_task_priority_values(self):
        """Test different priority values."""
        priorities = ["low", "medium", "high"]
        for i, priority in enumerate(priorities, 1):
            task = Task(task_id=i, title=f"Priority {priority}", priority=priority)
            assert task.priority == priority

    def test_task_completion_status(self):
        """Test task completion status."""
        active_task = Task(task_id=1, title="Active Task", completed=False)
        assert active_task.completed is False
        
        completed_task = Task(task_id=2, title="Completed Task", completed=True)
        assert completed_task.completed is True