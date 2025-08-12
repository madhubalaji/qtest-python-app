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
            description="This is a detailed description",
            priority="high",
            completed=True,
            created_at=created_at
        )
        
        assert task.id == 2
        assert task.title == "Important Task"
        assert task.description == "This is a detailed description"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == created_at

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            task_id=3,
            title="Dict Test",
            description="Test description",
            priority="low",
            completed=False,
            created_at="2023-01-01 10:00:00"
        )
        
        expected_dict = {
            "id": 3,
            "title": "Dict Test",
            "description": "Test description",
            "priority": "low",
            "completed": False,
            "created_at": "2023-01-01 10:00:00"
        }
        
        assert task.to_dict() == expected_dict

    def test_task_from_dict_complete(self):
        """Test creating task from complete dictionary."""
        task_data = {
            "id": 4,
            "title": "From Dict Task",
            "description": "Created from dictionary",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 15:00:00"
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 4
        assert task.title == "From Dict Task"
        assert task.description == "Created from dictionary"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == "2023-01-01 15:00:00"

    def test_task_from_dict_minimal(self):
        """Test creating task from minimal dictionary."""
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

    def test_task_str_representation_active(self):
        """Test string representation of active task."""
        task = Task(6, "Active Task", priority="high", completed=False)
        expected_str = "Task 6: Active Task (Active, high priority)"
        
        assert str(task) == expected_str

    def test_task_str_representation_completed(self):
        """Test string representation of completed task."""
        task = Task(7, "Completed Task", priority="low", completed=True)
        expected_str = "Task 7: Completed Task (Completed, low priority)"
        
        assert str(task) == expected_str

    def test_task_priority_values(self):
        """Test different priority values."""
        priorities = ["low", "medium", "high"]
        
        for i, priority in enumerate(priorities, 1):
            task = Task(i, f"Task {i}", priority=priority)
            assert task.priority == priority

    def test_task_completion_status(self):
        """Test task completion status changes."""
        task = Task(8, "Status Test")
        
        # Initially not completed
        assert task.completed is False
        
        # Mark as completed
        task.completed = True
        assert task.completed is True

    def test_task_created_at_auto_generation(self):
        """Test that created_at is automatically generated when not provided."""
        task = Task(9, "Auto Timestamp")
        
        # Should have a timestamp
        assert task.created_at is not None
        assert isinstance(task.created_at, str)
        
        # Should be a valid datetime format
        try:
            datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pytest.fail("created_at is not in expected datetime format")

    def test_task_id_types(self):
        """Test that task ID is properly handled."""
        task = Task(10, "ID Test")
        assert isinstance(task.id, int)
        assert task.id == 10

    def test_task_title_required(self):
        """Test that title is required and properly set."""
        task = Task(11, "Required Title")
        assert task.title == "Required Title"
        assert isinstance(task.title, str)

    def test_task_description_optional(self):
        """Test that description is optional."""
        task1 = Task(12, "No Description")
        assert task1.description == ""
        
        task2 = Task(13, "With Description", description="Has description")
        assert task2.description == "Has description"