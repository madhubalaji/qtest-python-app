"""
Tests for the TaskService class.
"""

import pytest
import os
import json
import tempfile
from unittest.mock import patch, mock_open

from src.models.task import Task
from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test class for TaskService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.service = TaskService(self.temp_file.name)

    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_add_task(self):
        """Test adding a new task."""
        task = self.service.add_task("Test Task", "Test Description", "high")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed is False

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks with incremental IDs."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")

        assert task1.id == 1
        assert task2.id == 2

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")

        tasks = self.service.get_all_tasks()
        assert len(tasks) == 2

    def test_get_all_tasks_filter_completed(self):
        """Test getting tasks with completed filter."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        self.service.complete_task(task1.id)

        # Get all tasks
        all_tasks = self.service.get_all_tasks(show_completed=True)
        assert len(all_tasks) == 2

        # Get only incomplete tasks
        incomplete_tasks = self.service.get_all_tasks(show_completed=False)
        assert len(incomplete_tasks) == 1
        assert incomplete_tasks[0].id == task2.id

    def test_get_task_by_id(self):
        """Test getting a task by ID."""
        task = self.service.add_task("Test Task")
        retrieved_task = self.service.get_task_by_id(task.id)

        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title

    def test_get_task_by_id_not_found(self):
        """Test getting a non-existent task by ID."""
        with pytest.raises(TaskNotFoundException):
            self.service.get_task_by_id(999)

    def test_update_task(self):
        """Test updating a task."""
        task = self.service.add_task("Original Title")
        updated_task = self.service.update_task(
            task.id,
            title="Updated Title",
            description="Updated Description",
            priority="high"
        )

        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == "high"

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.service.update_task(999, title="New Title")

    def test_complete_task(self):
        """Test marking a task as complete."""
        task = self.service.add_task("Test Task")
        completed_task = self.service.complete_task(task.id)

        assert completed_task.completed is True

    def test_complete_task_not_found(self):
        """Test completing a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.service.complete_task(999)

    def test_delete_task(self):
        """Test deleting a task."""
        task = self.service.add_task("Test Task")
        deleted_task = self.service.delete_task(task.id)

        assert deleted_task.id == task.id
        assert len(self.service.get_all_tasks()) == 0

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.service.delete_task(999)

    def test_search_tasks(self):
        """Test searching for tasks."""
        self.service.add_task("Python Programming", "Learn Python basics")
        self.service.add_task("Java Development", "Build Java application")
        self.service.add_task("Database Design", "Design database schema")

        # Search by title
        python_tasks = self.service.search_tasks("Python")
        assert len(python_tasks) == 1
        assert python_tasks[0].title == "Python Programming"

        # Search by description
        learn_tasks = self.service.search_tasks("Learn")
        assert len(learn_tasks) == 1

        # Search case insensitive
        java_tasks = self.service.search_tasks("java")
        assert len(java_tasks) == 1

    def test_search_tasks_no_results(self):
        """Test searching with no matching results."""
        self.service.add_task("Test Task")
        results = self.service.search_tasks("nonexistent")
        assert len(results) == 0

    @patch('os.path.exists')
    def test_load_tasks_invalid_json(self, mock_exists):
        """Test loading tasks from invalid JSON file."""
        mock_exists.return_value = True
        
        with patch('builtins.open', mock_open(read_data='invalid json')):
            with patch('builtins.print') as mock_print:
                service = TaskService("test.json")
                assert len(service.tasks) == 0
                mock_print.assert_called_once_with("Error reading task file. Starting with empty task list.")

    def test_persistence(self):
        """Test that tasks are persisted to file."""
        # Add a task
        task = self.service.add_task("Persistent Task")

        # Create a new service instance with the same file
        new_service = TaskService(self.temp_file.name)

        # Verify the task was loaded
        loaded_tasks = new_service.get_all_tasks()
        assert len(loaded_tasks) == 1
        assert loaded_tasks[0].title == "Persistent Task"