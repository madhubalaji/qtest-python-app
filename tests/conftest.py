"""
Pytest configuration and fixtures for the task manager tests.
"""

import os
import sys
import tempfile
import pytest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.task_service import TaskService
from src.models.task import Task


@pytest.fixture
def temp_storage_file():
    """Create a temporary storage file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def task_service(temp_storage_file):
    """Create a TaskService instance with temporary storage."""
    return TaskService(temp_storage_file)


@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task(
        task_id=1,
        title="Test Task",
        description="This is a test task",
        priority="medium",
        completed=False,
        created_at="2023-01-01 12:00:00"
    )


@pytest.fixture
def sample_tasks():
    """Create multiple sample tasks for testing."""
    return [
        Task(1, "Task 1", "Description 1", "high", False, "2023-01-01 12:00:00"),
        Task(2, "Task 2", "Description 2", "medium", True, "2023-01-02 12:00:00"),
        Task(3, "Task 3", "Description 3", "low", False, "2023-01-03 12:00:00")
    ]