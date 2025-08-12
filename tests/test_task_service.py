"""Tests for the TaskService class."""

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

    def test_task_service_initialization(self, temp_storage_file):
        """Test TaskService initialization."""
        service = TaskService(temp_storage_file)
        assert service.storage_file == temp_storage_file
        assert isinstance(service.tasks, list)
        assert len(service.tasks) == 0

    def test_add_task(self, task_service):
        """Test adding a new task."""
        task = task_service.add_task("Test Task", "Test Description", "high")
        
        assert isinstance(task, Task)
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed is False

    def test_add_multiple_tasks(self, task_service):
        """Test adding multiple tasks with incremental IDs."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task3 = task_service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_get_all_tasks(self, task_service):
        """Test getting all tasks."""
        task_service.add_task("Task 1")
        task_service.add_task("Task 2")
        
        tasks = task_service.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"

    def test_get_all_tasks_exclude_completed(self, task_service):
        """Test getting tasks excluding completed ones."""
        task1 = task_service.add_task("Active Task")
        task2 = task_service.add_task("Completed Task")
        task_service.complete_task(task2.id)
        
        active_tasks = task_service.get_all_tasks(show_completed=False)
        all_tasks = task_service.get_all_tasks(show_completed=True)
        
        assert len(active_tasks) == 1
        assert len(all_tasks) == 2
        assert active_tasks[0].title == "Active Task"

    def test_get_task_by_id(self, task_service):
        """Test getting a task by ID."""
        task = task_service.add_task("Find Me", "Description")
        
        found_task = task_service.get_task_by_id(task.id)
        assert found_task.id == task.id
        assert found_task.title == "Find Me"

    def test_get_task_by_id_not_found(self, task_service):
        """Test getting a non-existent task by ID."""
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(999)

    def test_update_task(self, task_service):
        """Test updating a task."""
        task = task_service.add_task("Original Title", "Original Description", "low")
        
        updated_task = task_service.update_task(
            task.id,
            title="Updated Title",
            description="Updated Description",
            priority="high"
        )
        
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == "high"

    def test_complete_task(self, task_service):
        """Test marking a task as complete."""
        task = task_service.add_task("Complete Me")
        assert task.completed is False
        
        completed_task = task_service.complete_task(task.id)
        assert completed_task.completed is True

    def test_delete_task(self, task_service):
        """Test deleting a task."""
        task = task_service.add_task("Delete Me")
        assert len(task_service.tasks) == 1
        
        deleted_task = task_service.delete_task(task.id)
        assert deleted_task.title == "Delete Me"
        assert len(task_service.tasks) == 0

    def test_delete_task_not_found(self, task_service):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service.delete_task(999)

    def test_search_tasks(self, task_service):
        """Test searching for tasks."""
        task_service.add_task("Python Programming", "Learn Python basics")
        task_service.add_task("Java Development", "Build Java application")
        task_service.add_task("Python Web App", "Create web app with Python")
        
        python_tasks = task_service.search_tasks("Python")
        java_tasks = task_service.search_tasks("Java")
        web_tasks = task_service.search_tasks("web")
        
        assert len(python_tasks) == 2
        assert len(java_tasks) == 1
        assert len(web_tasks) == 1

    def test_search_tasks_case_insensitive(self, task_service):
        """Test case-insensitive task search."""
        task_service.add_task("UPPERCASE TASK", "lowercase description")
        
        results = task_service.search_tasks("uppercase")
        assert len(results) == 1
        
        results = task_service.search_tasks("LOWERCASE")
        assert len(results) == 1

    def test_persistence(self, temp_storage_file):
        """Test that tasks are persisted to file."""
        # Create service and add tasks
        service1 = TaskService(temp_storage_file)
        service1.add_task("Persistent Task", "This should be saved")
        
        # Create new service instance with same file
        service2 = TaskService(temp_storage_file)
        tasks = service2.get_all_tasks()
        
        assert len(tasks) == 1
        assert tasks[0].title == "Persistent Task"
        assert tasks[0].description == "This should be saved"

    def test_load_tasks_from_corrupted_file(self, temp_storage_file):
        """Test loading tasks from a corrupted JSON file."""
        # Write invalid JSON to file
        with open(temp_storage_file, 'w') as f:
            f.write("invalid json content")
        
        # Should handle gracefully and start with empty list
        service = TaskService(temp_storage_file)
        assert len(service.tasks) == 0