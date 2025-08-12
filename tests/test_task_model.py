"""
Unit tests for the Task model.
"""

import pytest
from datetime import datetime
from src.models.task import Task


class TestTask:
    """Test cases for the Task model."""

    def test_task_initialization_with_defaults(self):
        """Test task initialization with default values."""
        task = Task(task_id=1, title="Test Task")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert task.created_at is not None
        assert isinstance(task.created_at, str)

    def test_task_initialization_with_all_parameters(self):
        """Test task initialization with all parameters provided."""
        created_at = "2023-01-01 12:00:00"
        task = Task(
            task_id=2,
            title="Complete Task",
            description="A detailed description",
            priority="high",
            completed=True,
            created_at=created_at
        )
        
        assert task.id == 2
        assert task.title == "Complete Task"
        assert task.description == "A detailed description"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == created_at

    def test_task_initialization_with_partial_parameters(self):
        """Test task initialization with some parameters provided."""
        task = Task(
            task_id=3,
            title="Partial Task",
            description="Some description",
            priority="low"
        )
        
        assert task.id == 3
        assert task.title == "Partial Task"
        assert task.description == "Some description"
        assert task.priority == "low"
        assert task.completed is False
        assert task.created_at is not None

    def test_to_dict_method(self):
        """Test converting task to dictionary."""
        created_at = "2023-01-01 12:00:00"
        task = Task(
            task_id=4,
            title="Dict Task",
            description="Task for dict test",
            priority="high",
            completed=True,
            created_at=created_at
        )
        
        expected_dict = {
            "id": 4,
            "title": "Dict Task",
            "description": "Task for dict test",
            "priority": "high",
            "completed": True,
            "created_at": created_at
        }
        
        assert task.to_dict() == expected_dict

    def test_from_dict_method_with_all_fields(self):
        """Test creating task from dictionary with all fields."""
        task_data = {
            "id": 5,
            "title": "From Dict Task",
            "description": "Created from dictionary",
            "priority": "low",
            "completed": False,
            "created_at": "2023-01-01 12:00:00"
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 5
        assert task.title == "From Dict Task"
        assert task.description == "Created from dictionary"
        assert task.priority == "low"
        assert task.completed is False
        assert task.created_at == "2023-01-01 12:00:00"

    def test_from_dict_method_with_minimal_fields(self):
        """Test creating task from dictionary with minimal required fields."""
        task_data = {
            "id": 6,
            "title": "Minimal Task"
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 6
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert task.created_at is None

    def test_from_dict_method_with_partial_fields(self):
        """Test creating task from dictionary with some optional fields."""
        task_data = {
            "id": 7,
            "title": "Partial Dict Task",
            "description": "Has description",
            "completed": True
        }
        
        task = Task.from_dict(task_data)
        
        assert task.id == 7
        assert task.title == "Partial Dict Task"
        assert task.description == "Has description"
        assert task.priority == "medium"  # default value
        assert task.completed is True
        assert task.created_at is None

    def test_str_method_active_task(self):
        """Test string representation of an active task."""
        task = Task(
            task_id=8,
            title="Active Task",
            priority="high",
            completed=False
        )
        
        expected_str = "Task 8: Active Task (Active, high priority)"
        assert str(task) == expected_str

    def test_str_method_completed_task(self):
        """Test string representation of a completed task."""
        task = Task(
            task_id=9,
            title="Completed Task",
            priority="low",
            completed=True
        )
        
        expected_str = "Task 9: Completed Task (Completed, low priority)"
        assert str(task) == expected_str

    def test_task_with_empty_title(self):
        """Test task creation with empty title."""
        task = Task(task_id=10, title="")
        
        assert task.id == 10
        assert task.title == ""
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False

    def test_task_with_long_title_and_description(self):
        """Test task creation with long title and description."""
        long_title = "A" * 1000
        long_description = "B" * 2000
        
        task = Task(
            task_id=11,
            title=long_title,
            description=long_description
        )
        
        assert task.id == 11
        assert task.title == long_title
        assert task.description == long_description

    def test_task_priority_values(self):
        """Test task creation with different priority values."""
        priorities = ["low", "medium", "high", "urgent", ""]
        
        for i, priority in enumerate(priorities, 12):
            task = Task(task_id=i, title=f"Task {i}", priority=priority)
            assert task.priority == priority

    def test_created_at_format(self):
        """Test that created_at follows expected datetime format."""
        task = Task(task_id=17, title="Time Test")
        
        # Check that created_at can be parsed as datetime
        try:
            datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pytest.fail("created_at is not in expected format")

    def test_task_roundtrip_dict_conversion(self):
        """Test that task can be converted to dict and back without data loss."""
        original_task = Task(
            task_id=18,
            title="Roundtrip Task",
            description="Test roundtrip conversion",
            priority="high",
            completed=True,
            created_at="2023-01-01 12:00:00"
        )
        
        # Convert to dict and back
        task_dict = original_task.to_dict()
        restored_task = Task.from_dict(task_dict)
        
        # Verify all attributes are preserved
        assert restored_task.id == original_task.id
        assert restored_task.title == original_task.title
        assert restored_task.description == original_task.description
        assert restored_task.priority == original_task.priority
        assert restored_task.completed == original_task.completed
        assert restored_task.created_at == original_task.created_at

    def test_task_equality_through_dict_comparison(self):
        """Test task equality by comparing their dictionary representations."""
        task1 = Task(
            task_id=19,
            title="Equal Task",
            description="Same content",
            priority="medium",
            completed=False,
            created_at="2023-01-01 12:00:00"
        )
        
        task2 = Task(
            task_id=19,
            title="Equal Task",
            description="Same content",
            priority="medium",
            completed=False,
            created_at="2023-01-01 12:00:00"
        )
        
        assert task1.to_dict() == task2.to_dict()

    def test_task_with_special_characters(self):
        """Test task creation with special characters in title and description."""
        special_title = "Task with émojis 🚀 and spëcial chars: @#$%^&*()"
        special_description = "Description with newlines\nand tabs\t and unicode: ñáéíóú"
        
        task = Task(
            task_id=20,
            title=special_title,
            description=special_description
        )
        
        assert task.title == special_title
        assert task.description == special_description
        
        # Test roundtrip conversion with special characters
        task_dict = task.to_dict()
        restored_task = Task.from_dict(task_dict)
        
        assert restored_task.title == special_title
        assert restored_task.description == special_description