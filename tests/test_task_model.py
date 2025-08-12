"""
Tests for the Task model class.
"""

import pytest
from datetime import datetime

from src.models.task import Task


class TestTask:
    """Test cases for Task model."""

    def test_task_creation_basic(self):
        """Test basic task creation."""
        task = Task(1, "Test Task", "Test Description", "high")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert not task.completed
        assert task.created_at is not None

    def test_task_creation_with_defaults(self):
        """Test task creation with default values."""
        task = Task(1, "Test Task")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert not task.completed
        assert task.created_at is not None

    def test_task_creation_with_all_params(self):
        """Test task creation with all parameters."""
        created_at = "2023-01-01 10:00:00"
        task = Task(
            task_id=1,
            title="Test Task",
            description="Test Description",
            priority="low",
            completed=True,
            created_at=created_at
        )
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "low"
        assert task.completed
        assert task.created_at == created_at

    def test_task_creation_auto_timestamp(self):
        """Test that created_at is automatically set if not provided."""
        task = Task(1, "Test Task")
        
        # Check that created_at is a valid timestamp string
        assert isinstance(task.created_at, str)
        assert len(task.created_at) > 0
        
        # Try to parse it as a datetime to verify format
        datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")

    def test_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            task_id=1,
            title="Test Task",
            description="Test Description",
            priority="high",
            completed=True,
            created_at="2023-01-01 10:00:00"
        )
        
        expected_dict = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 10:00:00"
        }
        
        assert task.to_dict() == expected_dict

    def test_from_dict_complete(self):
        """Test creating task from complete dictionary."""
        data = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 10:00:00"
        }
        
        task = Task.from_dict(data)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed
        assert task.created_at == "2023-01-01 10:00:00"

    def test_from_dict_minimal(self):
        """Test creating task from minimal dictionary."""
        data = {
            "id": 1,
            "title": "Test Task"
        }
        
        task = Task.from_dict(data)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert not task.completed
        assert task.created_at is not None

    def test_from_dict_partial(self):
        """Test creating task from partial dictionary."""
        data = {
            "id": 1,
            "title": "Test Task",
            "priority": "low",
            "completed": True
        }
        
        task = Task.from_dict(data)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "low"
        assert task.completed
        assert task.created_at is not None

    def test_str_representation_active(self):
        """Test string representation of active task."""
        task = Task(1, "Test Task", priority="high", completed=False)
        expected = "Task 1: Test Task (Active, high priority)"
        assert str(task) == expected

    def test_str_representation_completed(self):
        """Test string representation of completed task."""
        task = Task(1, "Test Task", priority="low", completed=True)
        expected = "Task 1: Test Task (Completed, low priority)"
        assert str(task) == expected

    def test_roundtrip_serialization(self):
        """Test that to_dict and from_dict are inverse operations."""
        original_task = Task(
            task_id=42,
            title="Original Task",
            description="Original Description",
            priority="medium",
            completed=False,
            created_at="2023-01-01 15:30:00"
        )
        
        # Convert to dict and back
        task_dict = original_task.to_dict()
        restored_task = Task.from_dict(task_dict)
        
        # Verify all attributes match
        assert restored_task.id == original_task.id
        assert restored_task.title == original_task.title
        assert restored_task.description == original_task.description
        assert restored_task.priority == original_task.priority
        assert restored_task.completed == original_task.completed
        assert restored_task.created_at == original_task.created_at

    def test_task_equality_by_attributes(self):
        """Test that tasks with same attributes are equivalent."""
        task1 = Task(1, "Test Task", "Description", "high", True, "2023-01-01 10:00:00")
        task2 = Task(1, "Test Task", "Description", "high", True, "2023-01-01 10:00:00")
        
        # While Task doesn't implement __eq__, we can check attributes
        assert task1.id == task2.id
        assert task1.title == task2.title
        assert task1.description == task2.description
        assert task1.priority == task2.priority
        assert task1.completed == task2.completed
        assert task1.created_at == task2.created_at