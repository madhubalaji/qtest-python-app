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

    def test_task_service_initialization(self):
        """Test TaskService initialization."""
        assert self.task_service.storage_file == self.temp_file.name
        assert isinstance(self.task_service.tasks, list)
        assert len(self.task_service.tasks) == 0

    def test_add_task(self):
        """Test adding a new task."""
        task = self.task_service.add_task(
            title="Test Task",
            description="Test Description",
            priority="high"
        )
        
        assert isinstance(task, Task)
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed is False
        assert len(self.task_service.tasks) == 1

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks with incremental IDs."""
        task1 = self.task_service.add_task("Task 1")
        task2 = self.task_service.add_task("Task 2")
        task3 = self.task_service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert len(self.task_service.tasks) == 3

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        self.task_service.add_task("Task 1")
        self.task_service.add_task("Task 2")
        
        all_tasks = self.task_service.get_all_tasks()
        assert len(all_tasks) == 2
        assert all_tasks[0].title == "Task 1"
        assert all_tasks[1].title == "Task 2"

    def test_get_all_tasks_with_completed_filter(self):
        """Test getting tasks with completed filter."""
        task1 = self.task_service.add_task("Active Task")
        task2 = self.task_service.add_task("Completed Task")
        self.task_service.complete_task(task2.id)
        
        # Get all tasks including completed
        all_tasks = self.task_service.get_all_tasks(show_completed=True)
        assert len(all_tasks) == 2
        
        # Get only active tasks
        active_tasks = self.task_service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 1
        assert active_tasks[0].title == "Active Task"

    def test_get_task_by_id(self):
        """Test getting a task by ID."""
        task = self.task_service.add_task("Test Task")
        retrieved_task = self.task_service.get_task_by_id(task.id)
        
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title

    def test_get_task_by_id_not_found(self):
        """Test getting a task by non-existent ID."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.get_task_by_id(999)

    def test_update_task(self):
        """Test updating a task."""
        task = self.task_service.add_task("Original Task")
        
        updated_task = self.task_service.update_task(
            task.id,
            title="Updated Task",
            description="Updated Description",
            priority="low",
            completed=True
        )
        
        assert updated_task.id == task.id
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == "low"
        assert updated_task.completed is True

    def test_update_task_partial(self):
        """Test updating a task with partial data."""
        task = self.task_service.add_task("Test Task", "Original Description", "medium")
        
        updated_task = self.task_service.update_task(task.id, title="New Title")
        
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Unchanged
        assert updated_task.priority == "medium"  # Unchanged

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.update_task(999, title="Non-existent")

    def test_complete_task(self):
        """Test marking a task as complete."""
        task = self.task_service.add_task("Test Task")
        assert task.completed is False
        
        completed_task = self.task_service.complete_task(task.id)
        assert completed_task.completed is True

    def test_complete_task_not_found(self):
        """Test completing a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.complete_task(999)

    def test_delete_task(self):
        """Test deleting a task."""
        task1 = self.task_service.add_task("Task 1")
        task2 = self.task_service.add_task("Task 2")
        
        assert len(self.task_service.tasks) == 2
        
        deleted_task = self.task_service.delete_task(task1.id)
        
        assert deleted_task.id == task1.id
        assert len(self.task_service.tasks) == 1
        assert self.task_service.tasks[0].id == task2.id

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.delete_task(999)

    def test_search_tasks(self):
        """Test searching for tasks."""
        self.task_service.add_task("Python Programming", "Learn Python basics")
        self.task_service.add_task("Java Development", "Build Java application")
        self.task_service.add_task("Database Design", "Design Python database")
        
        # Search by title
        python_tasks = self.task_service.search_tasks("Python")
        assert len(python_tasks) == 2
        
        # Search by description
        learn_tasks = self.task_service.search_tasks("Learn")
        assert len(learn_tasks) == 1
        
        # Case insensitive search
        java_tasks = self.task_service.search_tasks("java")
        assert len(java_tasks) == 1

    def test_search_tasks_no_results(self):
        """Test searching with no matching results."""
        self.task_service.add_task("Test Task")
        results = self.task_service.search_tasks("nonexistent")
        assert len(results) == 0

    def test_persistence_save_and_load(self):
        """Test that tasks are saved to and loaded from file."""
        # Add tasks
        task1 = self.task_service.add_task("Persistent Task 1")
        task2 = self.task_service.add_task("Persistent Task 2")
        
        # Create new service instance with same file
        new_service = TaskService(self.temp_file.name)
        
        # Check that tasks were loaded
        assert len(new_service.tasks) == 2
        assert new_service.tasks[0].title == "Persistent Task 1"
        assert new_service.tasks[1].title == "Persistent Task 2"

    def test_load_from_nonexistent_file(self):
        """Test loading from a non-existent file."""
        nonexistent_file = "/tmp/nonexistent_tasks.json"
        service = TaskService(nonexistent_file)
        assert len(service.tasks) == 0

    def test_load_from_corrupted_file(self):
        """Test loading from a corrupted JSON file."""
        # Write invalid JSON to file
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json content")
        
        # Should handle gracefully and start with empty list
        service = TaskService(self.temp_file.name)
        assert len(service.tasks) == 0

    def test_task_id_generation(self):
        """Test that task IDs are generated correctly."""
        # Add some tasks
        task1 = self.task_service.add_task("Task 1")
        task2 = self.task_service.add_task("Task 2")
        
        # Delete first task
        self.task_service.delete_task(task1.id)
        
        # Add new task - should get next available ID
        task3 = self.task_service.add_task("Task 3")
        assert task3.id == 3  # Should be 3, not reuse 1