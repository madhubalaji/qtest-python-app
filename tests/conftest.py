"""
Pytest configuration and fixtures for the task manager tests.
"""

import os
import tempfile
import pytest
from src.services.task_service import TaskService
from src.models.task import Task


@pytest.fixture
def temp_storage_file():
    """Create a temporary file for testing task storage."""
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
        completed=False
    )


@pytest.fixture
def sample_tasks():
    """Create multiple sample tasks for testing."""
    return [
        Task(1, "Task 1", "Description 1", "high", False),
        Task(2, "Task 2", "Description 2", "medium", True),
        Task(3, "Task 3", "Description 3", "low", False),
    ]