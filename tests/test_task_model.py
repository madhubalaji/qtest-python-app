"""
Tests for the Task model.
"""

import pytest
from src.models.task import Task


def test_task_creation():
    """Test creating a Task instance."""
    task = Task(1, "Test Task", "This is a test task", "high")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.priority == "high"
    assert not task.completed


def test_task_to_dict():
    """Test converting a Task to a dictionary."""
    task = Task(1, "Test Task", "This is a test task", "high")
    task_dict = task.to_dict()
    
    assert task_dict["id"] == 1
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == "This is a test task"
    assert task_dict["priority"] == "high"
    assert not task_dict["completed"]
    assert "created_at" in task_dict


def test_task_from_dict():
    """Test creating a Task from a dictionary."""
    task_dict = {
        "id": 2,
        "title": "Another Task",
        "description": "This is another test task",
        "priority": "low",
        "completed": True,
        "created_at": "2023-01-01 12:00:00"
    }
    
    task = Task.from_dict(task_dict)
    
    assert task.id == 2
    assert task.title == "Another Task"
    assert task.description == "This is another test task"
    assert task.priority == "low"
    assert task.completed
    assert task.created_at == "2023-01-01 12:00:00"


def test_task_str_representation():
    """Test the string representation of a Task."""
    task = Task(1, "Test Task", priority="medium")
    assert str(task) == "Task 1: Test Task (Active, medium priority)"
    
    task.completed = True
    assert str(task) == "Task 1: Test Task (Completed, medium priority)"