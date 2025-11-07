"""Tests for the Task model - additional test cases."""

from datetime import datetime
from src.models.task import Task


class TestTaskModel:
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
        """Test creating a task with all parameters."""
        created_at = "2023-01-01 12:00:00"
        task = Task(
            task_id=2,
            title="Complete Task",
            description="A complete task description",
            priority="high",
            completed=True,
            created_at=created_at
        )
        
        assert task.id == 2
        assert task.title == "Complete Task"
        assert task.description == "A complete task description"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == created_at

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            task_id=3,
            title="Dict Task",
            description="Task for dict test",
            priority="low",
            completed=False,
            created_at="2023-01-01 12:00:00"
        )
        
        expected_dict = {
            "id": 3,
            "title": "Dict Task",
            "description": "Task for dict test",
            "priority": "low",
            "completed": False,
            "created_at": "2023-01-01 12:00:00"
        }
        
        assert task.to_dict() == expected_dict

    def test_task_from_dict(self):
        """Test creating a task from dictionary."""
        task_dict = {
            "id": 4,
            "title": "From Dict Task",
            "description": "Created from dictionary",
            "priority": "high",
            "completed": True,
            "created_at": "2023-01-01 12:00:00"
        }
        
        task = Task.from_dict(task_dict)
        
        assert task.id == 4
        assert task.title == "From Dict Task"
        assert task.description == "Created from dictionary"
        assert task.priority == "high"
        assert task.completed is True
        assert task.created_at == "2023-01-01 12:00:00"

    def test_task_from_dict_with_missing_optional_fields(self):
        """Test creating a task from dictionary with missing optional fields."""
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
        assert task.created_at is not None

    def test_task_string_representation(self):
        """Test string representation of a task."""
        task = Task(task_id=6, title="String Task", priority="high", completed=False)
        expected_str = "Task 6: String Task (Active, high priority)"
        assert str(task) == expected_str
        
        task.completed = True
        expected_str = "Task 6: String Task (Completed, high priority)"
        assert str(task) == expected_str

    def test_task_created_at_auto_generation(self):
        """Test that created_at is automatically generated when not provided."""
        task = Task(task_id=7, title="Auto Time Task")
        
        # Check that created_at is set and is a valid datetime string
        assert task.created_at is not None
        assert len(task.created_at) > 0
        
        # Try to parse the datetime string to ensure it's valid
        datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")