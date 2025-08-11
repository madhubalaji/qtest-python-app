"""
Tests for the TaskService class.
"""

import pytest
import os
import tempfile
import json
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test cases for the TaskService class."""

    @pytest.fixture
    def temp_storage_file(self):
        """Create a temporary storage file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            yield f.name
        # Clean up after test
        if os.path.exists(f.name):
            os.unlink(f.name)

    @pytest.fixture
    def task_service(self, temp_storage_file):
        """Create a TaskService instance with temporary storage."""
        return TaskService(temp_storage_file)

    @pytest.fixture
    def populated_task_service(self, temp_storage_file):
        """Create a TaskService instance with some pre-populated tasks."""
        service = TaskService(temp_storage_file)
        service.add_task("Task 1", "Description 1", "high")
        service.add_task("Task 2", "Description 2", "medium")
        service.add_task("Task 3", "Description 3", "low")
        return service

    def test_task_service_initialization_empty_file(self, task_service):
        """Test TaskService initialization with empty storage."""
        assert len(task_service.tasks) == 0

    def test_task_service_initialization_nonexistent_file(self):
        """Test TaskService initialization with non-existent file."""
        service = TaskService("nonexistent_file.json")
        assert len(service.tasks) == 0

    def test_add_task(self, task_service):
        """Test adding a new task."""
        task = task_service.add_task("Test Task", "Test Description", "high")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed is False
        assert len(task_service.tasks) == 1

    def test_add_multiple_tasks_incremental_ids(self, task_service):
        """Test that task IDs increment correctly."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task3 = task_service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_get_all_tasks_show_completed(self, populated_task_service):
        """Test getting all tasks including completed ones."""
        # Complete one task
        populated_task_service.complete_task(1)
        
        all_tasks = populated_task_service.get_all_tasks(show_completed=True)
        assert len(all_tasks) == 3

    def test_get_all_tasks_hide_completed(self, populated_task_service):
        """Test getting all tasks excluding completed ones."""
        # Complete one task
        populated_task_service.complete_task(1)
        
        active_tasks = populated_task_service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 2
        assert all(not task.completed for task in active_tasks)

    def test_get_task_by_id_existing(self, populated_task_service):
        """Test getting an existing task by ID."""
        task = populated_task_service.get_task_by_id(2)
        assert task.id == 2
        assert task.title == "Task 2"

    def test_get_task_by_id_nonexistent(self, populated_task_service):
        """Test getting a non-existent task by ID."""
        with pytest.raises(TaskNotFoundException):
            populated_task_service.get_task_by_id(999)

    def test_update_task_title(self, populated_task_service):
        """Test updating a task's title."""
        updated_task = populated_task_service.update_task(1, title="Updated Title")
        assert updated_task.title == "Updated Title"
        assert updated_task.id == 1

    def test_update_task_multiple_fields(self, populated_task_service):
        """Test updating multiple fields of a task."""
        updated_task = populated_task_service.update_task(
            1,
            title="New Title",
            description="New Description",
            priority="low",
            completed=True
        )
        
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.priority == "low"
        assert updated_task.completed is True

    def test_update_task_nonexistent(self, populated_task_service):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            populated_task_service.update_task(999, title="New Title")

    def test_complete_task(self, populated_task_service):
        """Test marking a task as complete."""
        completed_task = populated_task_service.complete_task(1)
        assert completed_task.completed is True
        assert completed_task.id == 1

    def test_complete_task_nonexistent(self, populated_task_service):
        """Test completing a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            populated_task_service.complete_task(999)

    def test_delete_task_existing(self, populated_task_service):
        """Test deleting an existing task."""
        initial_count = len(populated_task_service.tasks)
        deleted_task = populated_task_service.delete_task(2)
        
        assert deleted_task.id == 2
        assert deleted_task.title == "Task 2"
        assert len(populated_task_service.tasks) == initial_count - 1
        
        # Verify task is actually removed
        with pytest.raises(TaskNotFoundException):
            populated_task_service.get_task_by_id(2)

    def test_delete_task_nonexistent(self, populated_task_service):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            populated_task_service.delete_task(999)

    def test_delete_task_preserves_other_tasks(self, populated_task_service):
        """Test that deleting a task doesn't affect other tasks."""
        # Get tasks before deletion
        task1 = populated_task_service.get_task_by_id(1)
        task3 = populated_task_service.get_task_by_id(3)
        
        # Delete middle task
        populated_task_service.delete_task(2)
        
        # Verify other tasks are still there and unchanged
        remaining_task1 = populated_task_service.get_task_by_id(1)
        remaining_task3 = populated_task_service.get_task_by_id(3)
        
        assert remaining_task1.title == task1.title
        assert remaining_task3.title == task3.title
        assert len(populated_task_service.tasks) == 2

    def test_search_tasks_by_title(self, populated_task_service):
        """Test searching tasks by title."""
        results = populated_task_service.search_tasks("Task 1")
        assert len(results) == 1
        assert results[0].title == "Task 1"

    def test_search_tasks_by_description(self, populated_task_service):
        """Test searching tasks by description."""
        results = populated_task_service.search_tasks("Description 2")
        assert len(results) == 1
        assert results[0].description == "Description 2"

    def test_search_tasks_case_insensitive(self, populated_task_service):
        """Test that search is case insensitive."""
        results = populated_task_service.search_tasks("TASK")
        assert len(results) == 3  # Should find all tasks

    def test_search_tasks_no_results(self, populated_task_service):
        """Test searching with no matching results."""
        results = populated_task_service.search_tasks("nonexistent")
        assert len(results) == 0

    def test_persistence_after_add(self, temp_storage_file):
        """Test that tasks are persisted after adding."""
        service1 = TaskService(temp_storage_file)
        service1.add_task("Persistent Task", "This should persist")
        
        # Create new service instance with same file
        service2 = TaskService(temp_storage_file)
        assert len(service2.tasks) == 1
        assert service2.tasks[0].title == "Persistent Task"

    def test_persistence_after_delete(self, temp_storage_file):
        """Test that task deletion is persisted."""
        service1 = TaskService(temp_storage_file)
        service1.add_task("Task 1")
        service1.add_task("Task 2")
        service1.delete_task(1)
        
        # Create new service instance with same file
        service2 = TaskService(temp_storage_file)
        assert len(service2.tasks) == 1
        assert service2.tasks[0].title == "Task 2"

    def test_load_tasks_corrupted_json(self, temp_storage_file):
        """Test loading tasks from corrupted JSON file."""
        # Write invalid JSON to file
        with open(temp_storage_file, 'w') as f:
            f.write("invalid json content")
        
        # Should handle gracefully and start with empty list
        service = TaskService(temp_storage_file)
        assert len(service.tasks) == 0