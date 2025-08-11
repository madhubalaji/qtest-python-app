"""
Tests for the Task model.
"""

import pytest
from datetime import datetime
from src.models.task import Task


class TestTask:
    """Test cases for the Task model."""

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(task_id=1, title="Test Task")
        
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
            description="This is an important task",
            priority="high",
            completed=True,
            created_at=created_at
        )
        
        assert task.id == 2
        assert task.title == "Important Task"
        assert task.description == "This is an important task"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == created_at

    def test_task_to_dict(self):
        """Test converting a task to dictionary."""
        task = Task(
            task_id=3,
            title="Dict Test",
            description="Testing dict conversion",
            priority="low",
            completed=False
        )
        
        task_dict = task.to_dict()
        
        assert task_dict["id"] == 3
        assert task_dict["title"] == "Dict Test"
        assert task_dict["description"] == "Testing dict conversion"
        assert task_dict["priority"] == "low"
        assert task_dict["completed"] is False
        assert "created_at" in task_dict

    def test_task_from_dict(self):
        """Test creating a task from dictionary."""
        task_data = {
            "id": 4,
            "title": "From Dict Task",
            "description": "Created from dictionary",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 10:00:00"
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 4
        assert task.title == "From Dict Task"
        assert task.description == "Created from dictionary"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == "2023-01-01 10:00:00"

    def test_task_from_dict_with_missing_optional_fields(self):
        """Test creating a task from dictionary with missing optional fields."""
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
        assert task.created_at is None

    def test_task_string_representation(self):
        """Test string representation of a task."""
        # Test active task
        active_task = Task(task_id=6, title="Active Task", priority="high")
        assert str(active_task) == "Task 6: Active Task (Active, high priority)"
        
        # Test completed task
        completed_task = Task(task_id=7, title="Completed Task", priority="low", completed=True)
        assert str(completed_task) == "Task 7: Completed Task (Completed, low priority)"

    def test_task_priority_validation(self):
        """Test that task accepts different priority values."""
        priorities = ["low", "medium", "high"]
        
        for i, priority in enumerate(priorities, 1):
            task = Task(task_id=i, title=f"Task {i}", priority=priority)
            assert task.priority == priority

    def test_task_created_at_auto_generation(self):
        """Test that created_at is automatically generated when not provided."""
        task = Task(task_id=8, title="Auto Timestamp Task")
        
        # Check that created_at is set and is a valid datetime string
        assert task.created_at is not None
        assert len(task.created_at) > 0
        
        # Try to parse the datetime string to ensure it's valid
        try:
            datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pytest.fail("created_at is not in the expected datetime format")