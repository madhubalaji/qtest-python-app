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
    def task_service_with_data(self, temp_storage_file):
        """Create a TaskService instance with some test data."""
        # Create test data
        test_tasks = [
            {
                "id": 1,
                "title": "Task 1",
                "description": "First task",
                "priority": "high",
                "completed": False,
                "created_at": "2023-01-01 12:00:00"
            },
            {
                "id": 2,
                "title": "Task 2",
                "description": "Second task",
                "priority": "medium",
                "completed": True,
                "created_at": "2023-01-02 12:00:00"
            },
            {
                "id": 3,
                "title": "Task 3",
                "description": "Third task",
                "priority": "low",
                "completed": False,
                "created_at": "2023-01-03 12:00:00"
            }
        ]
        
        # Write test data to file
        with open(temp_storage_file, 'w') as f:
            json.dump(test_tasks, f)
        
        return TaskService(temp_storage_file)

    def test_add_task(self, task_service):
        """Test adding a new task."""
        task = task_service.add_task("Test Task", "Test description", "high")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.priority == "high"
        assert task.completed is False
        
        # Verify task is in the service
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == 1

    def test_get_all_tasks(self, task_service_with_data):
        """Test getting all tasks."""
        tasks = task_service_with_data.get_all_tasks()
        assert len(tasks) == 3
        
        # Test filtering completed tasks
        active_tasks = task_service_with_data.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 2
        assert all(not task.completed for task in active_tasks)

    def test_get_task_by_id(self, task_service_with_data):
        """Test getting a task by ID."""
        task = task_service_with_data.get_task_by_id(1)
        assert task.id == 1
        assert task.title == "Task 1"

    def test_get_task_by_id_not_found(self, task_service_with_data):
        """Test getting a non-existent task by ID."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_data.get_task_by_id(999)

    def test_update_task(self, task_service_with_data):
        """Test updating a task."""
        updated_task = task_service_with_data.update_task(
            1, 
            title="Updated Task",
            description="Updated description",
            priority="low",
            completed=True
        )
        
        assert updated_task.id == 1
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated description"
        assert updated_task.priority == "low"
        assert updated_task.completed is True

    def test_update_task_not_found(self, task_service_with_data):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_data.update_task(999, title="Updated")

    def test_complete_task(self, task_service_with_data):
        """Test marking a task as complete."""
        task = task_service_with_data.complete_task(1)
        assert task.completed is True
        
        # Verify the task is actually updated
        updated_task = task_service_with_data.get_task_by_id(1)
        assert updated_task.completed is True

    def test_complete_task_not_found(self, task_service_with_data):
        """Test completing a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_data.complete_task(999)

    def test_delete_task(self, task_service_with_data):
        """Test deleting a task."""
        # Verify task exists before deletion
        task = task_service_with_data.get_task_by_id(2)
        assert task.id == 2
        
        # Delete the task
        deleted_task = task_service_with_data.delete_task(2)
        assert deleted_task.id == 2
        assert deleted_task.title == "Task 2"
        
        # Verify task is removed from the service
        all_tasks = task_service_with_data.get_all_tasks()
        assert len(all_tasks) == 2
        assert not any(task.id == 2 for task in all_tasks)
        
        # Verify we can't get the deleted task
        with pytest.raises(TaskNotFoundException):
            task_service_with_data.get_task_by_id(2)

    def test_delete_task_not_found(self, task_service_with_data):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_data.delete_task(999)

    def test_delete_all_tasks(self, task_service_with_data):
        """Test deleting all tasks one by one."""
        # Get initial count
        initial_tasks = task_service_with_data.get_all_tasks()
        assert len(initial_tasks) == 3
        
        # Delete all tasks
        for task in initial_tasks:
            task_service_with_data.delete_task(task.id)
        
        # Verify all tasks are deleted
        remaining_tasks = task_service_with_data.get_all_tasks()
        assert len(remaining_tasks) == 0

    def test_search_tasks(self, task_service_with_data):
        """Test searching for tasks."""
        # Search by title
        results = task_service_with_data.search_tasks("Task 1")
        assert len(results) == 1
        assert results[0].title == "Task 1"
        
        # Search by description
        results = task_service_with_data.search_tasks("First")
        assert len(results) == 1
        assert results[0].description == "First task"
        
        # Search case insensitive
        results = task_service_with_data.search_tasks("TASK")
        assert len(results) == 3
        
        # Search with no results
        results = task_service_with_data.search_tasks("nonexistent")
        assert len(results) == 0

    def test_persistence_after_operations(self, temp_storage_file):
        """Test that operations are persisted to storage file."""
        # Create service and add a task
        service1 = TaskService(temp_storage_file)
        task = service1.add_task("Persistent Task", "Test persistence")
        task_id = task.id
        
        # Create new service instance (simulating app restart)
        service2 = TaskService(temp_storage_file)
        
        # Verify task exists in new instance
        loaded_task = service2.get_task_by_id(task_id)
        assert loaded_task.title == "Persistent Task"
        assert loaded_task.description == "Test persistence"
        
        # Delete task and verify persistence
        service2.delete_task(task_id)
        
        # Create another new service instance
        service3 = TaskService(temp_storage_file)
        
        # Verify task is deleted
        with pytest.raises(TaskNotFoundException):
            service3.get_task_by_id(task_id)

    def test_load_tasks_with_corrupted_file(self, temp_storage_file):
        """Test loading tasks when storage file is corrupted."""
        # Write invalid JSON to file
        with open(temp_storage_file, 'w') as f:
            f.write("invalid json content")
        
        # Should handle gracefully and start with empty task list
        service = TaskService(temp_storage_file)
        tasks = service.get_all_tasks()
        assert len(tasks) == 0

    def test_load_tasks_with_nonexistent_file(self, temp_storage_file):
        """Test loading tasks when storage file doesn't exist."""
        # Remove the file if it exists
        if os.path.exists(temp_storage_file):
            os.unlink(temp_storage_file)
        
        # Should handle gracefully and start with empty task list
        service = TaskService(temp_storage_file)
        tasks = service.get_all_tasks()
        assert len(tasks) == 0