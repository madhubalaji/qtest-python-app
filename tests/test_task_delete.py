import os
import tempfile
import pytest
from src.services.task_service import TaskService

@pytest.fixture
def task_service():
    # Create a temporary file for testing
    fd, path = tempfile.mkstemp()
    os.close(fd)
    service = TaskService(storage_file=path)
    yield service
    # Cleanup after tests
    os.unlink(path)

def test_delete_task(task_service):
    # Create a task first
    task = task_service.add_task("Test Task", "Test Description")
    assert task.id is not None
    
    # Delete the task
    deleted_task = task_service.delete_task(task.id)
    assert deleted_task.id == task.id
    
    # Verify task is deleted
    tasks = task_service.get_all_tasks()
    assert len(tasks) == 0
    
    # Verify attempting to get deleted task raises exception
    with pytest.raises(Exception):
        task_service.get_task_by_id(task.id)