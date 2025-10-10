"""
Basic tests to ensure pytest runs without errors.
"""


def test_basic():
    """Basic test to ensure pytest finds at least one test."""
    assert True


def test_import_task_service():
    """Test that we can import the task service."""
    from src.services.task_service import TaskService
    assert TaskService is not None


def test_import_task_model():
    """Test that we can import the task model."""
    from src.models.task import Task
    assert Task is not None