"""
Tests for the Task model.
"""

import pytest
from datetime import datetime
from src.models.task import Task


class TestTask:
    """Test cases for the Task model."""

    def test_task_creation_with_all_parameters(self):
        """Test creating a task with all parameters."""
        created_at = "2023-01-01 12:00:00"
        task = Task(
            task_id=1,
            title="Test Task",
            description="Test Description",
            priority="high",
            completed=True,
            created_at=created_at
        )
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == created_at

    def test_task_creation_with_minimal_parameters(self):
        """Test creating a task with minimal parameters."""
        task = Task(task_id=1, title="Minimal Task")
        
        assert task.id == 1
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert task.created_at is not None

    def test_task_creation_auto_timestamp(self):
        """Test that created_at is automatically set if not provided."""
        task = Task(task_id=1, title="Test Task")
        
        # Check that created_at is a valid timestamp string
        assert task.created_at is not None
        assert len(task.created_at) > 0
        
        # Verify it can be parsed as a datetime
        datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            task_id=1,
            title="Test Task",
            description="Test Description",
            priority="high",
            completed=True,
            created_at="2023-01-01 12:00:00"
        )
        
        expected_dict = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 12:00:00"
        }
        
        assert task.to_dict() == expected_dict

    def test_task_from_dict_complete(self):
        """Test creating task from complete dictionary."""
        task_dict = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 12:00:00"
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
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
        assert task.created_at is None

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
        assert task.created_at is None

    def test_task_str_representation_active(self):
        """Test string representation of active task."""
        task = Task(
            task_id=1,
            title="Test Task",
            priority="high",
            completed=False
        )
        
        expected_str = "Task 1: Test Task (Active, high priority)"
        assert str(task) == expected_str

    def test_task_str_representation_completed(self):
        """Test string representation of completed task."""
        task = Task(
            task_id=2,
            title="Completed Task",
            priority="medium",
            completed=True
        )
        
        expected_str = "Task 2: Completed Task (Completed, medium priority)"
        assert str(task) == expected_str

    def test_task_roundtrip_serialization(self):
        """Test that task can be serialized and deserialized without data loss."""
        original_task = Task(
            task_id=1,
            title="Test Task",
            description="Test Description",
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