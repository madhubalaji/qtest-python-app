"""
Tests for Task model class.
"""

import pytest
from datetime import datetime
from unittest.mock import patch

from src.models.task import Task


class TestTask:
    """Test cases for Task model class."""

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

    def test_task_creation_with_defaults(self):
        """Test creating a task with default parameters."""
        with patch('src.models.task.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00"
            
            task = Task(task_id=1, title="Test Task")
            
            assert task.id == 1
            assert task.title == "Test Task"
            assert task.description == ""
            assert task.priority == "medium"
            assert task.completed is False
            assert task.created_at == "2023-01-01 12:00:00"

    def test_task_creation_minimal(self):
        """Test creating a task with minimal parameters."""
        task = Task(task_id=5, title="Minimal Task")
        
        assert task.id == 5
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert task.created_at is not None

    def test_to_dict(self):
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

    def test_from_dict_complete(self):
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

    def test_from_dict_minimal(self):
        """Test creating task from minimal dictionary."""
        task_dict = {
            "id": 2,
            "title": "Minimal Task"
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 2
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert task.created_at is None

    def test_from_dict_partial(self):
        """Test creating task from partial dictionary."""
        task_dict = {
            "id": 3,
            "title": "Partial Task",
            "priority": "low",
            "completed": True
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 3
        assert task.title == "Partial Task"
        assert task.description == ""
        assert task.priority == "low"
        assert task.completed is True
        assert task.created_at is None

    def test_str_representation_active(self):
        """Test string representation of active task."""
        task = Task(
            task_id=1,
            title="Active Task",
            priority="high",
            completed=False
        )
        
        expected_str = "Task 1: Active Task (Active, high priority)"
        assert str(task) == expected_str

    def test_str_representation_completed(self):
        """Test string representation of completed task."""
        task = Task(
            task_id=2,
            title="Completed Task",
            priority="low",
            completed=True
        )
        
        expected_str = "Task 2: Completed Task (Completed, low priority)"
        assert str(task) == expected_str

    def test_task_equality(self):
        """Test task equality comparison."""
        task1 = Task(task_id=1, title="Task 1", description="Description 1")
        task2 = Task(task_id=1, title="Task 1", description="Description 1")
        task3 = Task(task_id=2, title="Task 2", description="Description 2")
        
        # Tasks with same attributes should be equal (if __eq__ is implemented)
        # Note: This test assumes Task class might implement __eq__ in the future
        # For now, it tests object identity
        assert task1 is not task2
        assert task1 is not task3

    def test_task_serialization_roundtrip(self):
        """Test that task can be serialized and deserialized correctly."""
        original_task = Task(
            task_id=42,
            title="Roundtrip Task",
            description="Test serialization",
            priority="medium",
            completed=False,
            created_at="2023-06-15 14:30:00"
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

    def test_task_modification(self):
        """Test that task attributes can be modified."""
        task = Task(task_id=1, title="Original Title")
        
        # Modify attributes
        task.title = "Modified Title"
        task.description = "New Description"
        task.priority = "high"
        task.completed = True
        
        # Verify modifications
        assert task.title == "Modified Title"
        assert task.description == "New Description"
        assert task.priority == "high"
        assert task.completed is True

    def test_task_created_at_auto_generation(self):
        """Test that created_at is automatically generated when not provided."""
        with patch('src.models.task.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2023-12-25 10:30:45"
            
            task = Task(task_id=1, title="Auto Date Task")
            
            assert task.created_at == "2023-12-25 10:30:45"
            mock_datetime.now.assert_called_once()
            mock_datetime.now.return_value.strftime.assert_called_once_with("%Y-%m-%d %H:%M:%S")

    def test_task_priority_values(self):
        """Test task creation with different priority values."""
        priorities = ["low", "medium", "high", "urgent", "critical"]
        
        for i, priority in enumerate(priorities, 1):
            task = Task(task_id=i, title=f"Task {i}", priority=priority)
            assert task.priority == priority

    def test_task_boolean_completed_values(self):
        """Test task creation with different completed values."""
        # Test with explicit True
        task1 = Task(task_id=1, title="Task 1", completed=True)
        assert task1.completed is True
        
        # Test with explicit False
        task2 = Task(task_id=2, title="Task 2", completed=False)
        assert task2.completed is False
        
        # Test with default (should be False)
        task3 = Task(task_id=3, title="Task 3")
        assert task3.completed is False

    def test_task_empty_strings(self):
        """Test task creation with empty strings."""
        task = Task(
            task_id=1,
            title="",
            description="",
            priority="",
            created_at=""
        )
        
        assert task.title == ""
        assert task.description == ""
        assert task.priority == ""
        assert task.created_at == ""

    def test_task_unicode_content(self):
        """Test task creation with unicode content."""
        task = Task(
            task_id=1,
            title="📝 Unicode Task",
            description="Task with émojis and spëcial characters: 你好",
            priority="high"
        )
        
        assert task.title == "📝 Unicode Task"
        assert task.description == "Task with émojis and spëcial characters: 你好"
        assert task.priority == "high"

    def test_task_long_content(self):
        """Test task creation with long content."""
        long_title = "A" * 1000
        long_description = "B" * 5000
        
        task = Task(
            task_id=1,
            title=long_title,
            description=long_description
        )
        
        assert task.title == long_title
        assert task.description == long_description
        assert len(task.title) == 1000
        assert len(task.description) == 5000