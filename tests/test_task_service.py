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
    def sample_tasks(self, task_service):
        """Create sample tasks for testing."""
        task1 = task_service.add_task("Task 1", "Description 1", "high")
        task2 = task_service.add_task("Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Task 3", "Description 3", "low")
        return [task1, task2, task3]

    def test_task_service_initialization_empty_file(self, temp_storage_file):
        """Test TaskService initialization with non-existent file."""
        service = TaskService(temp_storage_file)
        assert len(service.tasks) == 0

    def test_task_service_initialization_with_existing_data(self, temp_storage_file):
        """Test TaskService initialization with existing data."""
        # Create test data
        test_data = [
            {
                "id": 1,
                "title": "Existing Task",
                "description": "Pre-existing task",
                "priority": "medium",
                "completed": False,
                "created_at": "2023-01-01 12:00:00"
            }
        ]
        
        with open(temp_storage_file, 'w') as f:
            json.dump(test_data, f)
        
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

    def test_add_task_with_defaults(self, task_service):
        """Test adding a task with default values."""
        task = task_service.add_task("Default Task")
        
        assert task.title == "Default Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False

    def test_add_multiple_tasks_incremental_ids(self, task_service):
        """Test that task IDs increment correctly."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task3 = task_service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_get_all_tasks(self, task_service, sample_tasks):
        """Test getting all tasks."""
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 3
        assert all([task in all_tasks for task in sample_tasks])

    def test_get_all_tasks_show_completed_false(self, task_service, sample_tasks):
        """Test getting tasks with completed tasks filtered out."""
        # Mark one task as completed
        task_service.complete_task(sample_tasks[0].id)
        
        active_tasks = task_service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 2
        assert all(not task.completed for task in active_tasks)

    def test_get_task_by_id(self, task_service, sample_tasks):
        """Test getting a task by ID."""
        task_id = sample_tasks[1].id
        retrieved_task = task_service.get_task_by_id(task_id)
        
        assert retrieved_task.id == task_id
        assert retrieved_task.title == sample_tasks[1].title

    def test_get_task_by_id_not_found(self, task_service):
        """Test getting a non-existent task by ID."""
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(999)

    def test_update_task(self, task_service, sample_tasks):
        """Test updating a task."""
        task_id = sample_tasks[0].id
        updated_task = task_service.update_task(
            task_id,
            title="Updated Title",
            description="Updated Description",
            priority="low",
            completed=True
        )
        
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == "low"
        assert updated_task.completed is True

    def test_update_task_partial(self, task_service, sample_tasks):
        """Test updating only some fields of a task."""
        task_id = sample_tasks[0].id
        original_description = sample_tasks[0].description
        
        updated_task = task_service.update_task(task_id, title="New Title Only")
        
        assert updated_task.title == "New Title Only"
        assert updated_task.description == original_description  # Should remain unchanged

    def test_update_task_not_found(self, task_service):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service.update_task(999, title="Non-existent")

    def test_complete_task(self, task_service, sample_tasks):
        """Test marking a task as complete."""
        task_id = sample_tasks[0].id
        completed_task = task_service.complete_task(task_id)
        
        assert completed_task.completed is True
        assert completed_task.id == task_id

    def test_complete_task_not_found(self, task_service):
        """Test completing a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service.complete_task(999)

    def test_delete_task(self, task_service, sample_tasks):
        """Test deleting a task."""
        task_id = sample_tasks[1].id
        original_count = len(task_service.tasks)
        
        deleted_task = task_service.delete_task(task_id)
        
        assert deleted_task.id == task_id
        assert len(task_service.tasks) == original_count - 1
        
        # Verify task is no longer in the list
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(task_id)

    def test_delete_task_not_found(self, task_service):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service.delete_task(999)

    def test_delete_all_tasks(self, task_service, sample_tasks):
        """Test deleting all tasks one by one."""
        original_count = len(sample_tasks)
        
        for i, task in enumerate(sample_tasks):
            task_service.delete_task(task.id)
            assert len(task_service.tasks) == original_count - (i + 1)
        
        assert len(task_service.tasks) == 0

    def test_search_tasks(self, task_service, sample_tasks):
        """Test searching for tasks."""
        # Add a task with specific content for searching
        task_service.add_task("Special Task", "This has special content")
        
        # Search by title
        results = task_service.search_tasks("Special")
        assert len(results) == 1
        assert results[0].title == "Special Task"
        
        # Search by description
        results = task_service.search_tasks("special content")
        assert len(results) == 1
        
        # Search case insensitive
        results = task_service.search_tasks("SPECIAL")
        assert len(results) == 1

    def test_search_tasks_no_results(self, task_service, sample_tasks):
        """Test searching with no matching results."""
        results = task_service.search_tasks("nonexistent")
        assert len(results) == 0

    def test_search_tasks_multiple_results(self, task_service):
        """Test searching with multiple matching results."""
        task_service.add_task("Test Task 1", "Testing description")
        task_service.add_task("Test Task 2", "Another test")
        task_service.add_task("Different Task", "No match here")
        
        results = task_service.search_tasks("test")
        assert len(results) == 2

    def test_persistence_after_operations(self, temp_storage_file):
        """Test that operations are persisted to storage."""
        # Create service and add tasks
        service1 = TaskService(temp_storage_file)
        task1 = service1.add_task("Persistent Task", "Should be saved")
        task2 = service1.add_task("Another Task", "Also saved")
        
        # Create new service instance with same file
        service2 = TaskService(temp_storage_file)
        
        # Verify tasks were loaded
        assert len(service2.tasks) == 2
        loaded_task = service2.get_task_by_id(task1.id)
        assert loaded_task.title == "Persistent Task"

    def test_persistence_after_delete(self, temp_storage_file):
        """Test that deletions are persisted to storage."""
        # Create service and add tasks
        service1 = TaskService(temp_storage_file)
        task1 = service1.add_task("Task to Delete")
        task2 = service1.add_task("Task to Keep")
        
        # Delete one task
        service1.delete_task(task1.id)
        
        # Create new service instance
        service2 = TaskService(temp_storage_file)
        
        # Verify deletion was persisted
        assert len(service2.tasks) == 1
        assert service2.tasks[0].title == "Task to Keep"
        
        with pytest.raises(TaskNotFoundException):
            service2.get_task_by_id(task1.id)

    def test_corrupted_storage_file_handling(self, temp_storage_file):
        """Test handling of corrupted storage file."""
        # Write invalid JSON to file
        with open(temp_storage_file, 'w') as f:
            f.write("invalid json content")
        
        # Should handle gracefully and start with empty task list
        service = TaskService(temp_storage_file)
        assert len(service.tasks) == 0