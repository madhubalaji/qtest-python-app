"""
Tests for the TaskService class.
"""

import os
import tempfile
import json
import pytest

from src.models.task import Task
from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test cases for TaskService."""

    @pytest.fixture
    def temp_storage_file(self):
        """Create a temporary storage file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write('[]')  # Empty task list
            temp_file = f.name
        yield temp_file
        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)

    @pytest.fixture
    def task_service(self, temp_storage_file):
        """Create a TaskService instance with temporary storage."""
        return TaskService(temp_storage_file)

    @pytest.fixture
    def task_service_with_tasks(self, temp_storage_file):
        """Create a TaskService instance with some pre-existing tasks."""
        # Create some initial tasks
        initial_tasks = [
            {"id": 1, "title": "Task 1", "description": "Description 1", "priority": "high", "completed": False, "created_at": "2023-01-01 10:00:00"},
            {"id": 2, "title": "Task 2", "description": "Description 2", "priority": "medium", "completed": False, "created_at": "2023-01-01 11:00:00"},
            {"id": 3, "title": "Task 3", "description": "Description 3", "priority": "low", "completed": True, "created_at": "2023-01-01 12:00:00"}
        ]
        
        with open(temp_storage_file, 'w') as f:
            json.dump(initial_tasks, f)
        
        return TaskService(temp_storage_file)

    def test_init_empty_storage(self, task_service):
        """Test TaskService initialization with empty storage."""
        assert len(task_service.tasks) == 0
        assert task_service._next_id == 1

    def test_init_with_existing_tasks(self, task_service_with_tasks):
        """Test TaskService initialization with existing tasks."""
        assert len(task_service_with_tasks.tasks) == 3
        assert task_service_with_tasks._next_id == 4  # Next ID should be 4

    def test_add_task_basic(self, task_service):
        """Test adding a basic task."""
        task = task_service.add_task("Test Task", "Test Description", "high")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert not task.completed
        assert len(task_service.tasks) == 1

    def test_add_task_default_values(self, task_service):
        """Test adding a task with default values."""
        task = task_service.add_task("Test Task")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert not task.completed

    def test_add_multiple_tasks_id_increment(self, task_service):
        """Test that task IDs increment correctly."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task3 = task_service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert len(task_service.tasks) == 3

    def test_get_all_tasks_show_completed(self, task_service_with_tasks):
        """Test getting all tasks including completed ones."""
        tasks = task_service_with_tasks.get_all_tasks(show_completed=True)
        assert len(tasks) == 3

    def test_get_all_tasks_hide_completed(self, task_service_with_tasks):
        """Test getting all tasks excluding completed ones."""
        tasks = task_service_with_tasks.get_all_tasks(show_completed=False)
        assert len(tasks) == 2
        assert all(not task.completed for task in tasks)

    def test_get_task_by_id_existing(self, task_service_with_tasks):
        """Test getting an existing task by ID."""
        task = task_service_with_tasks.get_task_by_id(1)
        assert task.id == 1
        assert task.title == "Task 1"

    def test_get_task_by_id_non_existing(self, task_service_with_tasks):
        """Test getting a non-existing task by ID."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_tasks.get_task_by_id(999)

    def test_update_task_title(self, task_service_with_tasks):
        """Test updating a task's title."""
        updated_task = task_service_with_tasks.update_task(1, title="Updated Title")
        assert updated_task.title == "Updated Title"
        assert updated_task.id == 1

    def test_update_task_multiple_fields(self, task_service_with_tasks):
        """Test updating multiple task fields."""
        updated_task = task_service_with_tasks.update_task(
            1, 
            title="New Title", 
            description="New Description", 
            priority="low",
            completed=True
        )
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.priority == "low"
        assert updated_task.completed

    def test_update_task_non_existing(self, task_service_with_tasks):
        """Test updating a non-existing task."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_tasks.update_task(999, title="New Title")

    def test_complete_task(self, task_service_with_tasks):
        """Test marking a task as complete."""
        completed_task = task_service_with_tasks.complete_task(1)
        assert completed_task.completed
        assert completed_task.id == 1

    def test_complete_task_non_existing(self, task_service_with_tasks):
        """Test completing a non-existing task."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_tasks.complete_task(999)

    def test_delete_task_existing(self, task_service_with_tasks):
        """Test deleting an existing task."""
        initial_count = len(task_service_with_tasks.tasks)
        deleted_task = task_service_with_tasks.delete_task(2)
        
        assert deleted_task.id == 2
        assert deleted_task.title == "Task 2"
        assert len(task_service_with_tasks.tasks) == initial_count - 1
        
        # Verify task is actually removed
        with pytest.raises(TaskNotFoundException):
            task_service_with_tasks.get_task_by_id(2)

    def test_delete_task_non_existing(self, task_service_with_tasks):
        """Test deleting a non-existing task."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_tasks.delete_task(999)

    def test_delete_and_add_new_task_id_generation(self, task_service_with_tasks):
        """Test that new task IDs are generated correctly after deletions."""
        # Delete some tasks
        task_service_with_tasks.delete_task(1)
        task_service_with_tasks.delete_task(3)
        
        # Add a new task
        new_task = task_service_with_tasks.add_task("New Task", "New Description")
        
        # New task should get the next available ID (4, since max was 3)
        assert new_task.id == 4

    def test_search_tasks_by_title(self, task_service_with_tasks):
        """Test searching tasks by title."""
        results = task_service_with_tasks.search_tasks("Task 1")
        assert len(results) == 1
        assert results[0].title == "Task 1"

    def test_search_tasks_by_description(self, task_service_with_tasks):
        """Test searching tasks by description."""
        results = task_service_with_tasks.search_tasks("Description 2")
        assert len(results) == 1
        assert results[0].description == "Description 2"

    def test_search_tasks_case_insensitive(self, task_service_with_tasks):
        """Test that search is case insensitive."""
        results = task_service_with_tasks.search_tasks("TASK 1")
        assert len(results) == 1
        assert results[0].title == "Task 1"

    def test_search_tasks_no_results(self, task_service_with_tasks):
        """Test searching with no matching results."""
        results = task_service_with_tasks.search_tasks("Non-existent")
        assert len(results) == 0

    def test_search_tasks_multiple_results(self, task_service_with_tasks):
        """Test searching with multiple matching results."""
        results = task_service_with_tasks.search_tasks("Task")
        assert len(results) == 3  # All tasks contain "Task"

    def test_persistence_after_add(self, task_service):
        """Test that tasks are persisted after adding."""
        task_service.add_task("Persistent Task")
        
        # Create a new service instance with the same storage file
        new_service = TaskService(task_service.storage_file)
        assert len(new_service.tasks) == 1
        assert new_service.tasks[0].title == "Persistent Task"

    def test_persistence_after_delete(self, task_service_with_tasks):
        """Test that tasks are persisted after deletion."""
        task_service_with_tasks.delete_task(1)
        
        # Create a new service instance with the same storage file
        new_service = TaskService(task_service_with_tasks.storage_file)
        assert len(new_service.tasks) == 2
        
        # Verify the deleted task is not present
        task_ids = [task.id for task in new_service.tasks]
        assert 1 not in task_ids
        assert 2 in task_ids
        assert 3 in task_ids