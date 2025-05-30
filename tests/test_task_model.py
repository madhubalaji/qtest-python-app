"""
Tests for the Task model.
"""
import pytest
from datetime import datetime
from src.models.task import Task


def test_task_creation():
    """Test task creation with minimal parameters."""
    task = Task(1, "Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.priority == "medium"
    assert task.completed is False
    assert task.created_at is not None


def test_task_creation_with_all_parameters():
    """Test task creation with all parameters."""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task = Task(
        1, 
        "Test Task", 
        "Test Description", 
        "high", 
        True, 
        created_at
    )
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "high"
    assert task.completed is True
    assert task.created_at == created_at


def test_task_to_dict():
    """Test converting task to dictionary."""
    task = Task(1, "Test Task")
    task_dict = task.to_dict()
    assert task_dict["id"] == 1
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == ""
    assert task_dict["priority"] == "medium"
    assert task_dict["completed"] is False
    assert "created_at" in task_dict


def test_task_from_dict():
    """Test creating task from dictionary."""
    task_data = {
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "priority": "high",
        "completed": True,
        "created_at": "2023-04-11 10:29:17"
    }
    task = Task.from_dict(task_data)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "high"
    assert task.completed is True
    assert task.created_at == "2023-04-11 10:29:17"