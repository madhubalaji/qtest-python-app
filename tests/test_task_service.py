"""
Tests for the TaskService class.
"""

import os
import json
import pytest
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


@pytest.fixture
def temp_task_file(tmp_path):
    """Create a temporary task file for testing."""
    task_file = tmp_path / "test_tasks.json"
    tasks = [
        {
            "id": 1,
            "title": "Test Task 1",
            "description": "Description 1",
            "priority": "high",
            "completed": False,
            "created_at": "2023-01-01 10:00:00"
        },
        {
            "id": 2,
            "title": "Test Task 2",
            "description": "Description 2",
            "priority": "medium",
            "completed": True,
            "created_at": "2023-01-02 11:00:00"
        }
    ]
    
    with open(task_file, "w") as f:
        json.dump(tasks, f)
    
    return str(task_file)


@pytest.fixture
def task_service(temp_task_file):
    """Create a TaskService instance with the temporary task file."""
    return TaskService(temp_task_file)


def test_load_tasks(task_service):
    """Test loading tasks from a file."""
    tasks = task_service.tasks
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[0].title == "Test Task 1"
    assert tasks[1].id == 2
    assert tasks[1].title == "Test Task 2"


def test_add_task(task_service):
    """Test adding a new task."""
    task = task_service.add_task("New Task", "New Description", "low")
    
    assert task.id == 3
    assert task.title == "New Task"
    assert task.description == "New Description"
    assert task.priority == "low"
    assert not task.completed
    
    # Verify the task was added to the list
    tasks = task_service.get_all_tasks()
    assert len(tasks) == 3
    assert tasks[2].id == 3
    assert tasks[2].title == "New Task"


def test_get_all_tasks(task_service):
    """Test getting all tasks."""
    all_tasks = task_service.get_all_tasks()
    assert len(all_tasks) == 2
    
    # Test filtering out completed tasks
    active_tasks = task_service.get_all_tasks(show_completed=False)
    assert len(active_tasks) == 1
    assert active_tasks[0].id == 1


def test_get_task_by_id(task_service):
    """Test getting a task by ID."""
    task = task_service.get_task_by_id(1)
    assert task.id == 1
    assert task.title == "Test Task 1"
    
    # Test getting a non-existent task
    with pytest.raises(TaskNotFoundException):
        task_service.get_task_by_id(999)


def test_update_task(task_service):
    """Test updating a task."""
    task = task_service.update_task(1, title="Updated Title", priority="low")
    
    assert task.id == 1
    assert task.title == "Updated Title"
    assert task.priority == "low"
    
    # Verify the task was updated in the list
    updated_task = task_service.get_task_by_id(1)
    assert updated_task.title == "Updated Title"
    assert updated_task.priority == "low"


def test_complete_task(task_service):
    """Test marking a task as complete."""
    task = task_service.complete_task(1)
    
    assert task.id == 1
    assert task.completed
    
    # Verify the task was updated in the list
    completed_task = task_service.get_task_by_id(1)
    assert completed_task.completed


def test_delete_task(task_service):
    """Test deleting a task."""
    task = task_service.delete_task(1)
    
    assert task.id == 1
    
    # Verify the task was removed from the list
    tasks = task_service.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == 2
    
    # Test deleting a non-existent task
    with pytest.raises(TaskNotFoundException):
        task_service.delete_task(1)


def test_search_tasks(task_service):
    """Test searching for tasks."""
    # Add another task for testing search
    task_service.add_task("Search Test", "This is a searchable task")
    
    # Search by title
    results = task_service.search_tasks("Search")
    assert len(results) == 1
    assert results[0].title == "Search Test"
    
    # Search by description
    results = task_service.search_tasks("searchable")
    assert len(results) == 1
    assert results[0].description == "This is a searchable task"
    
    # Search with no results
    results = task_service.search_tasks("nonexistent")
    assert len(results) == 0