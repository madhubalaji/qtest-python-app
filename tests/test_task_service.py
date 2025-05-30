"""
Tests for the TaskService class.
"""
import pytest
import json
import os
from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


@pytest.fixture
def temp_storage_file(tmp_path):
    """Create a temporary storage file for testing."""
    storage_file = tmp_path / "test_tasks.json"
    with open(storage_file, "w") as f:
        json.dump([], f)
    return storage_file


def test_add_task(temp_storage_file):
    """Test adding a new task."""
    service = TaskService(str(temp_storage_file))
    task = service.add_task("Test Task", "Test Description", "high")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "high"


def test_get_all_tasks(temp_storage_file):
    """Test retrieving all tasks."""
    service = TaskService(str(temp_storage_file))
    task1 = service.add_task("Task 1")
    task2 = service.add_task("Task 2")
    tasks = service.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_get_task_by_id(temp_storage_file):
    """Test retrieving a task by ID."""
    service = TaskService(str(temp_storage_file))
    task = service.add_task("Test Task")
    retrieved_task = service.get_task_by_id(task.id)
    assert retrieved_task.id == task.id
    assert retrieved_task.title == task.title


def test_get_task_by_id_not_found(temp_storage_file):
    """Test retrieving a non-existent task."""
    service = TaskService(str(temp_storage_file))
    with pytest.raises(TaskNotFoundException):
        service.get_task_by_id(1)


def test_update_task(temp_storage_file):
    """Test updating a task."""
    service = TaskService(str(temp_storage_file))
    task = service.add_task("Test Task")
    updated_task = service.update_task(
        task.id,
        title="Updated Task",
        description="Updated Description",
        priority="high"
    )
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated Description"
    assert updated_task.priority == "high"


def test_complete_task(temp_storage_file):
    """Test marking a task as complete."""
    service = TaskService(str(temp_storage_file))
    task = service.add_task("Test Task")
    completed_task = service.complete_task(task.id)
    assert completed_task.completed is True


def test_delete_task(temp_storage_file):
    """Test deleting a task."""
    service = TaskService(str(temp_storage_file))
    task = service.add_task("Test Task")
    deleted_task = service.delete_task(task.id)
    assert deleted_task.id == task.id
    with pytest.raises(TaskNotFoundException):
        service.get_task_by_id(task.id)


def test_search_tasks(temp_storage_file):
    """Test searching for tasks."""
    service = TaskService(str(temp_storage_file))
    task1 = service.add_task("Test Task", "Test Description")
    task2 = service.add_task("Another Task", "Another Description")
    tasks = service.search_tasks("Test")
    assert len(tasks) == 1
    assert tasks[0].id == task1.id