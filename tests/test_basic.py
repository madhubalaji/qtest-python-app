"""Basic tests for the task manager application."""

import pytest
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.task import Task
from src.services.task_service import TaskService


def test_task_creation():
    """Test basic task creation."""
    task = Task(1, "Test Task", "Test Description", "medium")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "medium"
    assert task.completed is False


def test_task_service_initialization():
    """Test task service initialization."""
    # Use a temporary file for testing
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        task_service = TaskService(temp_file)
        assert task_service.storage_file == temp_file
        assert isinstance(task_service.tasks, list)
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_add_task():
    """Test adding a task."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        task_service = TaskService(temp_file)
        task = task_service.add_task("Test Task", "Test Description", "high")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert len(task_service.tasks) == 1
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)