"""
Basic tests for the Task model to ensure CI pipeline passes.
"""

import pytest
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.task import Task


def test_task_creation():
    """Test basic task creation."""
    task = Task(1, "Test Task", "Test Description", "medium")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.severity == "medium"
    assert not task.completed


def test_task_with_priority_compatibility():
    """Test backward compatibility with priority parameter."""
    task = Task(1, "Test Task", "Test Description", priority="high")
    assert task.severity == "high"


def test_task_to_dict():
    """Test task serialization to dictionary."""
    task = Task(1, "Test Task", "Test Description", "low")
    task_dict = task.to_dict()
    
    assert task_dict["id"] == 1
    assert task_dict["title"] == "Test Task"
    assert task_dict["severity"] == "low"
    assert "severity" in task_dict
    assert task_dict["completed"] is False


def test_task_from_dict():
    """Test task deserialization from dictionary."""
    task_data = {
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "severity": "high",
        "completed": False
    }
    
    task = Task.from_dict(task_data)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.severity == "high"


def test_task_from_dict_with_priority():
    """Test task deserialization with legacy priority field."""
    task_data = {
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "priority": "medium",
        "completed": False
    }
    
    task = Task.from_dict(task_data)
    assert task.id == 1
    assert task.severity == "medium"  # MIGRATION AUTOMATIQUE DE PRIORITY VERS SEVERITY