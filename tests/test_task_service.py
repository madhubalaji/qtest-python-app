"""
Tests for the TaskService class.
"""

import os
import json
import tempfile
import pytest
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test cases for the TaskService class."""

    @pytest.fixture
    def temp_storage_file(self):
        """Create a temporary file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
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
    def populated_task_service(self, temp_storage_file):
        """Create a TaskService with some pre-populated tasks."""
        service = TaskService(temp_storage_file)
        service.add_task("Task 1", "Description 1", "high")
        service.add_task("Task 2", "Description 2", "medium")
        service.add_task("Task 3", "Description 3", "low")
        return service

    def test_task_service_initialization_empty(self, task_service):
        """Test TaskService initialization with empty storage."""
        assert len(task_service.tasks) == 0

    def test_task_service_initialization_with_existing_file(self, temp_storage_file):
        """Test TaskService initialization with existing task file."""
        # Create a file with some tasks
        tasks_data = [
            {
                "id": 1,
                "title": "Existing Task",
                "description": "This task already exists",
                "priority": "medium",
                "completed": False,
                "created_at": "2023-01-01 12:00:00"
            }
        ]
        
        with open(temp_storage_file, 'w') as f:
            json.dump(tasks_data, f)
        
        service = TaskService(temp_storage_file)
        assert len(service.tasks) == 1
        assert service.tasks[0].title == "Existing Task"

    def test_add_task(self, task_service):
        """Test adding a new task."""
        task = task_service.add_task("New Task", "Task description", "high")
        
        assert task.id == 1
        assert task.title == "New Task"
        assert task.description == "Task description"
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
        # Mark one task as completed
        populated_task_service.complete_task(1)
        
        all_tasks = populated_task_service.get_all_tasks(show_completed=True)
        assert len(all_tasks) == 3

    def test_get_all_tasks_hide_completed(self, populated_task_service):
        """Test getting all tasks excluding completed ones."""
        # Mark one task as completed
        populated_task_service.complete_task(1)
        
        active_tasks = populated_task_service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 2
        assert all(not task.completed for task in active_tasks)

    def test_get_task_by_id_existing(self, populated_task_service):
        """Test getting a task by existing ID."""
        task = populated_task_service.get_task_by_id(2)
        assert task.id == 2
        assert task.title == "Task 2"

    def test_get_task_by_id_non_existing(self, populated_task_service):
        """Test getting a task by non-existing ID."""
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

    def test_update_task_non_existing(self, populated_task_service):
        """Test updating a non-existing task."""
        with pytest.raises(TaskNotFoundException):
            populated_task_service.update_task(999, title="New Title")

    def test_complete_task(self, populated_task_service):
        """Test marking a task as complete."""
        task = populated_task_service.complete_task(1)
        assert task.completed is True
        assert task.id == 1

    def test_complete_task_non_existing(self, populated_task_service):
        """Test completing a non-existing task."""
        with pytest.raises(TaskNotFoundException):
            populated_task_service.complete_task(999)

    def test_delete_task(self, populated_task_service):
        """Test deleting a task."""
        initial_count = len(populated_task_service.tasks)
        deleted_task = populated_task_service.delete_task(2)
        
        assert deleted_task.id == 2
        assert len(populated_task_service.tasks) == initial_count - 1
        
        # Verify the task is actually deleted
        with pytest.raises(TaskNotFoundException):
            populated_task_service.get_task_by_id(2)

    def test_delete_task_non_existing(self, populated_task_service):
        """Test deleting a non-existing task."""
        with pytest.raises(TaskNotFoundException):
            populated_task_service.delete_task(999)

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

    def test_search_tasks_partial_match(self, populated_task_service):
        """Test searching with partial matches."""
        results = populated_task_service.search_tasks("Task")
        assert len(results) == 3  # Should find all tasks with "Task" in title

    def test_search_tasks_no_results(self, populated_task_service):
        """Test searching with no matching results."""
        results = populated_task_service.search_tasks("NonExistent")
        assert len(results) == 0

    def test_persistence_after_add(self, temp_storage_file):
        """Test that tasks are persisted after adding."""
        service1 = TaskService(temp_storage_file)
        service1.add_task("Persistent Task", "This should persist")
        
        # Create a new service instance with the same file
        service2 = TaskService(temp_storage_file)
        assert len(service2.tasks) == 1
        assert service2.tasks[0].title == "Persistent Task"

    def test_persistence_after_update(self, temp_storage_file):
        """Test that task updates are persisted."""
        service1 = TaskService(temp_storage_file)
        task = service1.add_task("Original Title")
        service1.update_task(task.id, title="Updated Title")
        
        # Create a new service instance with the same file
        service2 = TaskService(temp_storage_file)
        assert service2.tasks[0].title == "Updated Title"

    def test_persistence_after_delete(self, temp_storage_file):
        """Test that task deletions are persisted."""
        service1 = TaskService(temp_storage_file)
        task1 = service1.add_task("Task 1")
        task2 = service1.add_task("Task 2")
        service1.delete_task(task1.id)
        
        # Create a new service instance with the same file
        service2 = TaskService(temp_storage_file)
        assert len(service2.tasks) == 1
        assert service2.tasks[0].title == "Task 2"

    def test_load_tasks_with_corrupted_json(self, temp_storage_file):
        """Test loading tasks when JSON file is corrupted."""
        # Write invalid JSON to the file
        with open(temp_storage_file, 'w') as f:
            f.write("invalid json content")
        
        # Should handle the error gracefully and start with empty list
        service = TaskService(temp_storage_file)
        assert len(service.tasks) == 0