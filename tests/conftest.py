"""
Pytest configuration file for the task manager tests.
"""

import os
import tempfile
import pytest
from src.services.task_service import TaskService


@pytest.fixture
def temp_storage_file():
    """Create a temporary file for task storage."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    yield temp_file.name
    os.unlink(temp_file.name)


@pytest.fixture
def task_service(temp_storage_file):
    """Create a TaskService instance with a temporary storage file."""
    return TaskService(temp_storage_file)


@pytest.fixture
def populated_task_service(task_service):
    """Create a TaskService instance with some pre-populated tasks."""
    task_service.add_task("Task 1", "Description 1", "low")
    task_service.add_task("Task 2", "Description 2", "medium")
    task_service.add_task("Task 3", "Description 3", "high")
    return task_service