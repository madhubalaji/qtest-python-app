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
        return TaskService(storage_file=temp_storage_file)

    @pytest.fixture
    def task_service_with_data(self, temp_storage_file):
        """Create a TaskService instance with some initial data."""
        # Create initial data
        initial_tasks = [
            {
                "id": 1,
                "title": "Task 1",
                "description": "First task",
                "priority": "high",
                "completed": False,
                "created_at": "2023-01-01 10:00:00"
            },
            {
                "id": 2,
                "title": "Task 2",
                "description": "Second task",
                "priority": "medium",
                "completed": True,
                "created_at": "2023-01-01 11:00:00"
            }
        ]
        
        with open(temp_storage_file, 'w') as f:
            json.dump(initial_tasks, f)
        
        return TaskService(storage_file=temp_storage_file)

    def test_task_service_initialization_empty_file(self, task_service):
        """Test TaskService initialization with empty/non-existent file."""
        assert len(task_service.tasks) == 0

    def test_task_service_initialization_with_data(self, task_service_with_data):
        """Test TaskService initialization with existing data."""
        assert len(task_service_with_data.tasks) == 2
        assert task_service_with_data.tasks[0].title == "Task 1"
        assert task_service_with_data.tasks[1].title == "Task 2"

    def test_add_task(self, task_service):
        """Test adding a new task."""
        task = task_service.add_task("New Task", "Task description", "high")
        
        assert task.id == 1
        assert task.title == "New Task"
        assert task.description == "Task description"
        assert task.priority == "high"
        assert task.completed is False
        assert len(task_service.tasks) == 1

    def test_add_multiple_tasks(self, task_service):
        """Test adding multiple tasks with auto-incrementing IDs."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task3 = task_service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert len(task_service.tasks) == 3

    def test_get_all_tasks_show_completed(self, task_service_with_data):
        """Test getting all tasks including completed ones."""
        tasks = task_service_with_data.get_all_tasks(show_completed=True)
        assert len(tasks) == 2

    def test_get_all_tasks_hide_completed(self, task_service_with_data):
        """Test getting all tasks excluding completed ones."""
        tasks = task_service_with_data.get_all_tasks(show_completed=False)
        assert len(tasks) == 1
        assert tasks[0].completed is False

    def test_get_task_by_id_existing(self, task_service_with_data):
        """Test getting a task by existing ID."""
        task = task_service_with_data.get_task_by_id(1)
        assert task.id == 1
        assert task.title == "Task 1"

    def test_get_task_by_id_non_existing(self, task_service_with_data):
        """Test getting a task by non-existing ID."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_data.get_task_by_id(999)

    def test_update_task_title(self, task_service_with_data):
        """Test updating a task's title."""
        updated_task = task_service_with_data.update_task(1, title="Updated Title")
        assert updated_task.title == "Updated Title"
        assert updated_task.id == 1

    def test_update_task_multiple_fields(self, task_service_with_data):
        """Test updating multiple fields of a task."""
        updated_task = task_service_with_data.update_task(
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

    def test_update_task_non_existing(self, task_service_with_data):
        """Test updating a non-existing task."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_data.update_task(999, title="New Title")

    def test_complete_task(self, task_service_with_data):
        """Test marking a task as complete."""
        task = task_service_with_data.complete_task(1)
        assert task.completed is True
        assert task.id == 1

    def test_complete_task_non_existing(self, task_service_with_data):
        """Test completing a non-existing task."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_data.complete_task(999)

    def test_delete_task(self, task_service_with_data):
        """Test deleting a task."""
        initial_count = len(task_service_with_data.tasks)
        deleted_task = task_service_with_data.delete_task(1)
        
        assert deleted_task.id == 1
        assert len(task_service_with_data.tasks) == initial_count - 1
        
        # Verify task is actually deleted
        with pytest.raises(TaskNotFoundException):
            task_service_with_data.get_task_by_id(1)

    def test_delete_task_non_existing(self, task_service_with_data):
        """Test deleting a non-existing task."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_data.delete_task(999)

    def test_search_tasks_by_title(self, task_service_with_data):
        """Test searching tasks by title."""
        results = task_service_with_data.search_tasks("Task 1")
        assert len(results) == 1
        assert results[0].title == "Task 1"

    def test_search_tasks_by_description(self, task_service_with_data):
        """Test searching tasks by description."""
        results = task_service_with_data.search_tasks("First")
        assert len(results) == 1
        assert results[0].description == "First task"

    def test_search_tasks_case_insensitive(self, task_service_with_data):
        """Test that search is case insensitive."""
        results = task_service_with_data.search_tasks("TASK")
        assert len(results) == 2  # Should find both tasks

    def test_search_tasks_no_results(self, task_service_with_data):
        """Test searching with no matching results."""
        results = task_service_with_data.search_tasks("nonexistent")
        assert len(results) == 0

    def test_persistence_after_add(self, task_service, temp_storage_file):
        """Test that tasks are persisted after adding."""
        task_service.add_task("Persistent Task")
        
        # Create a new service instance to test persistence
        new_service = TaskService(storage_file=temp_storage_file)
        assert len(new_service.tasks) == 1
        assert new_service.tasks[0].title == "Persistent Task"

    def test_persistence_after_update(self, task_service_with_data, temp_storage_file):
        """Test that tasks are persisted after updating."""
        task_service_with_data.update_task(1, title="Updated Persistent Task")
        
        # Create a new service instance to test persistence
        new_service = TaskService(storage_file=temp_storage_file)
        task = new_service.get_task_by_id(1)
        assert task.title == "Updated Persistent Task"

    def test_persistence_after_delete(self, task_service_with_data, temp_storage_file):
        """Test that tasks are persisted after deleting."""
        task_service_with_data.delete_task(1)
        
        # Create a new service instance to test persistence
        new_service = TaskService(storage_file=temp_storage_file)
        assert len(new_service.tasks) == 1
        with pytest.raises(TaskNotFoundException):
            new_service.get_task_by_id(1)

    def test_load_tasks_with_corrupted_json(self, temp_storage_file):
        """Test loading tasks when JSON file is corrupted."""
        # Write invalid JSON to the file
        with open(temp_storage_file, 'w') as f:
            f.write("invalid json content")
        
        # Should handle the error gracefully and start with empty list
        service = TaskService(storage_file=temp_storage_file)
        assert len(service.tasks) == 0