"""
Tests for the TaskService class.
"""

import os
import tempfile
import pytest
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test class for TaskService functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.task_service = TaskService(self.temp_file.name)

    def teardown_method(self):
        """Clean up after each test method."""
        # Remove the temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_add_task(self):
        """Test adding a new task."""
        task = self.task_service.add_task("Test Task", "Test Description", "high")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert not task.completed

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        # Add some tasks
        self.task_service.add_task("Task 1", "Description 1", "low")
        self.task_service.add_task("Task 2", "Description 2", "medium")
        
        tasks = self.task_service.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"

    def test_get_task_by_id(self):
        """Test getting a task by ID."""
        task = self.task_service.add_task("Test Task", "Test Description", "medium")
        
        retrieved_task = self.task_service.get_task_by_id(task.id)
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title

    def test_get_task_by_id_not_found(self):
        """Test getting a task by ID that doesn't exist."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.get_task_by_id(999)

    def test_complete_task(self):
        """Test marking a task as complete."""
        task = self.task_service.add_task("Test Task", "Test Description", "medium")
        
        completed_task = self.task_service.complete_task(task.id)
        assert completed_task.completed is True

    def test_delete_task(self):
        """Test deleting a task."""
        task = self.task_service.add_task("Test Task", "Test Description", "medium")
        
        # Verify task exists
        assert len(self.task_service.get_all_tasks()) == 1
        
        # Delete the task
        deleted_task = self.task_service.delete_task(task.id)
        
        # Verify task was deleted
        assert deleted_task.id == task.id
        assert len(self.task_service.get_all_tasks()) == 0
        
        # Verify task can't be found anymore
        with pytest.raises(TaskNotFoundException):
            self.task_service.get_task_by_id(task.id)

    def test_delete_task_not_found(self):
        """Test deleting a task that doesn't exist."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.delete_task(999)

    def test_update_task(self):
        """Test updating a task."""
        task = self.task_service.add_task("Test Task", "Test Description", "medium")
        
        updated_task = self.task_service.update_task(
            task.id,
            title="Updated Task",
            description="Updated Description",
            priority="high"
        )
        
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == "high"

    def test_search_tasks(self):
        """Test searching for tasks."""
        self.task_service.add_task("Python Task", "Learn Python programming", "high")
        self.task_service.add_task("Java Task", "Learn Java programming", "medium")
        self.task_service.add_task("Web Development", "Build a website", "low")
        
        # Search by title
        results = self.task_service.search_tasks("Python")
        assert len(results) == 1
        assert results[0].title == "Python Task"
        
        # Search by description
        results = self.task_service.search_tasks("programming")
        assert len(results) == 2
        
        # Search with no results
        results = self.task_service.search_tasks("nonexistent")
        assert len(results) == 0

    def test_persistence(self):
        """Test that tasks are persisted to file."""
        # Add a task
        task = self.task_service.add_task("Persistent Task", "This should persist", "medium")
        
        # Create a new service instance with the same file
        new_service = TaskService(self.temp_file.name)
        
        # Verify the task was loaded
        tasks = new_service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Persistent Task"
        assert tasks[0].id == task.id