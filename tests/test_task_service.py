"""
Tests for TaskService class.
"""

import os
import tempfile
import pytest
from unittest.mock import patch

from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test cases for TaskService class."""

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
        assert len(self.task_service.tasks) == 1

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        # Add some tasks
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        
        all_tasks = self.task_service.get_all_tasks()
        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 in all_tasks

    def test_get_all_tasks_filter_completed(self):
        """Test getting tasks with completed filter."""
        # Add tasks and complete one
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        self.task_service.complete_task(task1.id)
        
        # Get all tasks
        all_tasks = self.task_service.get_all_tasks(show_completed=True)
        assert len(all_tasks) == 2
        
        # Get only incomplete tasks
        incomplete_tasks = self.task_service.get_all_tasks(show_completed=False)
        assert len(incomplete_tasks) == 1
        assert task2 in incomplete_tasks
        assert task1 not in incomplete_tasks

    def test_get_task_by_id(self):
        """Test getting a task by ID."""
        task = self.task_service.add_task("Test Task", "Test Description", "medium")
        
        retrieved_task = self.task_service.get_task_by_id(task.id)
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title

    def test_get_task_by_id_not_found(self):
        """Test getting a task by non-existent ID."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.get_task_by_id(999)

    def test_update_task(self):
        """Test updating a task."""
        task = self.task_service.add_task("Original Title", "Original Description", "low")
        
        updated_task = self.task_service.update_task(
            task.id,
            title="Updated Title",
            description="Updated Description",
            priority="high",
            completed=True
        )
        
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == "high"
        assert updated_task.completed

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.update_task(999, title="New Title")

    def test_complete_task(self):
        """Test completing a task."""
        task = self.task_service.add_task("Test Task", "Test Description", "medium")
        
        completed_task = self.task_service.complete_task(task.id)
        assert completed_task.completed
        assert completed_task.id == task.id

    def test_complete_task_not_found(self):
        """Test completing a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.complete_task(999)

    def test_delete_task(self):
        """Test deleting a task."""
        # Add multiple tasks
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        task3 = self.task_service.add_task("Task 3", "Description 3", "high")
        
        assert len(self.task_service.tasks) == 3
        
        # Delete the middle task
        deleted_task = self.task_service.delete_task(task2.id)
        
        # Verify the task was deleted
        assert deleted_task.id == task2.id
        assert deleted_task.title == task2.title
        assert len(self.task_service.tasks) == 2
        assert task2 not in self.task_service.tasks
        assert task1 in self.task_service.tasks
        assert task3 in self.task_service.tasks

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.delete_task(999)

    def test_delete_task_single_task(self):
        """Test deleting the only task in the list."""
        task = self.task_service.add_task("Only Task", "Only Description", "medium")
        
        assert len(self.task_service.tasks) == 1
        
        deleted_task = self.task_service.delete_task(task.id)
        
        assert deleted_task.id == task.id
        assert len(self.task_service.tasks) == 0

    def test_delete_completed_task(self):
        """Test deleting a completed task."""
        task = self.task_service.add_task("Test Task", "Test Description", "medium")
        self.task_service.complete_task(task.id)
        
        assert task.completed
        assert len(self.task_service.tasks) == 1
        
        deleted_task = self.task_service.delete_task(task.id)
        
        assert deleted_task.completed
        assert len(self.task_service.tasks) == 0

    def test_delete_task_persistence(self):
        """Test that task deletion persists to storage."""
        # Add tasks
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        
        # Delete one task
        self.task_service.delete_task(task1.id)
        
        # Create a new service instance with the same file
        new_service = TaskService(self.temp_file.name)
        
        # Verify the deletion persisted
        assert len(new_service.tasks) == 1
        assert new_service.tasks[0].id == task2.id
        assert new_service.tasks[0].title == task2.title

    def test_search_tasks(self):
        """Test searching for tasks."""
        # Add tasks with different content
        task1 = self.task_service.add_task("Python Project", "Learn Python programming", "high")
        task2 = self.task_service.add_task("Java Assignment", "Complete Java homework", "medium")
        task3 = self.task_service.add_task("Meeting Notes", "Take notes during Python meeting", "low")
        
        # Search for "python" (case insensitive)
        results = self.task_service.search_tasks("python")
        assert len(results) == 2
        assert task1 in results
        assert task3 in results
        assert task2 not in results
        
        # Search for "java"
        results = self.task_service.search_tasks("java")
        assert len(results) == 1
        assert task2 in results

    def test_search_tasks_empty_result(self):
        """Test searching with no matching results."""
        self.task_service.add_task("Task 1", "Description 1", "low")
        
        results = self.task_service.search_tasks("nonexistent")
        assert len(results) == 0

    def test_load_tasks_file_not_exists(self):
        """Test loading tasks when file doesn't exist."""
        non_existent_file = "/tmp/non_existent_tasks.json"
        service = TaskService(non_existent_file)
        
        assert len(service.tasks) == 0

    def test_load_tasks_invalid_json(self):
        """Test loading tasks with invalid JSON."""
        # Create a file with invalid JSON
        invalid_json_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        invalid_json_file.write("invalid json content")
        invalid_json_file.close()
        
        try:
            with patch('builtins.print') as mock_print:
                service = TaskService(invalid_json_file.name)
                assert len(service.tasks) == 0
                mock_print.assert_called_once()
        finally:
            os.unlink(invalid_json_file.name)

    def test_task_id_generation(self):
        """Test that task IDs are generated correctly."""
        # Add tasks and verify IDs are sequential
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        task3 = self.task_service.add_task("Task 3", "Description 3", "high")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        
        # Delete middle task and add new one
        self.task_service.delete_task(task2.id)
        task4 = self.task_service.add_task("Task 4", "Description 4", "low")
        
        # New task should get the next available ID
        assert task4.id == 4

    def test_delete_task_order_preservation(self):
        """Test that deleting tasks preserves the order of remaining tasks."""
        # Add tasks in order
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        task3 = self.task_service.add_task("Task 3", "Description 3", "high")
        task4 = self.task_service.add_task("Task 4", "Description 4", "low")
        
        # Delete the second task
        self.task_service.delete_task(task2.id)
        
        # Verify remaining tasks are in correct order
        remaining_tasks = self.task_service.get_all_tasks()
        assert len(remaining_tasks) == 3
        assert remaining_tasks[0].id == task1.id
        assert remaining_tasks[1].id == task3.id
        assert remaining_tasks[2].id == task4.id