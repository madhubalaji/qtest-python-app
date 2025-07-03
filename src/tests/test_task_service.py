import os
import pytest
from src.services.task_service import TaskService

@pytest.fixture
def task_service():
    # Use a test-specific file
    test_file = "test_tasks.json"
    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)
    # Create service instance
    service = TaskService(test_file)
    yield service
    # Clean up after tests
    if os.path.exists(test_file):
        os.remove(test_file)

def test_delete_task(task_service):
    # Arrange
    task = task_service.add_task("Test Task")
    initial_task_count = len(task_service.get_all_tasks())
    
    # Act
    deleted_task = task_service.delete_task(task.id)
    
    # Assert
    assert deleted_task.id == task.id
    assert len(task_service.get_all_tasks()) == initial_task_count - 1
    # Verify task is actually deleted
    with pytest.raises(ValueError):
        task_service.get_task_by_id(task.id)

def test_delete_nonexistent_task(task_service):
    # Arrange & Act & Assert
    with pytest.raises(ValueError):
        task_service.delete_task(999)