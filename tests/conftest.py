"""
Pytest configuration file for the task manager application tests.
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import MagicMock

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.task import Task
from src.services.task_service import TaskService


@pytest.fixture
def sample_tasks():
    """Fixture providing sample tasks for testing."""
    return [
        Task(1, "Task 1", "Description 1", "low", False, "2023-01-01 12:00:00"),
        Task(2, "Task 2", "Description 2", "medium", False, "2023-01-02 12:00:00"),
        Task(3, "Task 3", "Description 3", "high", True, "2023-01-03 12:00:00"),
    ]


@pytest.fixture
def temp_storage_file():
    """Fixture providing a temporary file for task storage."""
    temp_file = tempfile.NamedTemporaryFile(delete=False).name
    yield temp_file
    # Clean up after the test
    if os.path.exists(temp_file):
        os.remove(temp_file)


@pytest.fixture
def task_service(temp_storage_file):
    """Fixture providing a TaskService instance with a temporary storage file."""
    return TaskService(temp_storage_file)


@pytest.fixture
def mock_task_service():
    """Fixture providing a mock TaskService."""
    mock_service = MagicMock(spec=TaskService)
    return mock_service