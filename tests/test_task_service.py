import pytest
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException

@pytest.fixture
def task_service():
    return TaskService(storage_file=":memory:")

def test_delete_task(task_service):
    # Create a test task
    task = task_service.add_task("Test Task", "Test Description")
    
    # Store the task ID
    task_id = task.id
    
    # Delete the task
    deleted_task = task_service.delete_task(task_id)
    
    # Verify deletion
    assert deleted_task.id == task_id
    assert deleted_task.title == "Test Task"
    
    # Verify task no longer exists in storage
    tasks = task_service.get_all_tasks()
    assert len(tasks) == 0
    
    # Verify attempting to get the deleted task raises an exception
    with pytest.raises(TaskNotFoundException):
        task_service.get_task_by_id(task_id)