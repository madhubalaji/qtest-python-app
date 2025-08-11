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
        """Test converting a task to dictionary."""
        task = Task(
            task_id=3,
            title="Dict Test",
            description="Test description",
            priority="low",
            completed=False
        )
        
        task_dict = task.to_dict()
        
        assert task_dict["id"] == 3
        assert task_dict["title"] == "Dict Test"
        assert task_dict["description"] == "Test description"
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
        assert task.created_at is not None

    def test_task_string_representation_active(self):
        """Test string representation of an active task."""
        task = Task(6, "Active Task", priority="high", completed=False)
        task_str = str(task)
        
        assert "Task 6: Active Task (Active, high priority)" == task_str

    def test_task_string_representation_completed(self):
        """Test string representation of a completed task."""
        task = Task(7, "Completed Task", priority="low", completed=True)
        task_str = str(task)
        
        assert "Task 7: Completed Task (Completed, low priority)" == task_str

    def test_task_created_at_auto_generation(self):
        """Test that created_at is automatically generated when not provided."""
        task = Task(8, "Auto Date Task")
        
        # Check that created_at is a valid datetime string
        try:
            datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pytest.fail("created_at should be a valid datetime string")

    def test_task_priority_validation(self):
        """Test that task accepts different priority values."""
        priorities = ["low", "medium", "high"]
        
        for i, priority in enumerate(priorities, 1):
            task = Task(i, f"Task {i}", priority=priority)
            assert task.priority == priority

    def test_task_roundtrip_dict_conversion(self):
        """Test that task can be converted to dict and back without data loss."""
        original_task = Task(
            task_id=9,
            title="Roundtrip Task",
            description="Test roundtrip conversion",
            priority="medium",
            completed=False,
            created_at="2023-01-01 15:30:00"
        )
        
        # Convert to dict and back
        task_dict = original_task.to_dict()
        restored_task = Task.from_dict(task_dict)
        
        # Verify all fields match
        assert restored_task.id == original_task.id
        assert restored_task.title == original_task.title
        assert restored_task.description == original_task.description
        assert restored_task.priority == original_task.priority
        assert restored_task.completed == original_task.completed
        assert restored_task.created_at == original_task.created_at