"""
Tests for the TaskService class.
"""

import os
import tempfile
import pytest
from unittest.mock import patch, mock_open
from src.models.task import Task
from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test cases for the TaskService class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.write('[]')
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
        assert task.completed is False

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks with incremental IDs."""
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        task3 = self.task_service.add_task("Task 3", "Description 3", "high")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        self.task_service.add_task("Task 1", "Description 1", "low")
        self.task_service.add_task("Task 2", "Description 2", "medium")
        
        tasks = self.task_service.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"

    def test_get_all_tasks_filter_completed(self):
        """Test getting tasks with completed filter."""
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        
        # Complete one task
        self.task_service.complete_task(task1.id)
        
        # Get all tasks including completed
        all_tasks = self.task_service.get_all_tasks(show_completed=True)
        assert len(all_tasks) == 2
        
        # Get only active tasks
        active_tasks = self.task_service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 1
        assert active_tasks[0].id == task2.id

    def test_get_task_by_id(self):
        """Test getting a task by ID."""
        task = self.task_service.add_task("Test Task", "Test Description", "high")
        retrieved_task = self.task_service.get_task_by_id(task.id)
        
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title
        assert retrieved_task.description == task.description
        assert retrieved_task.priority == task.priority

    def test_get_task_by_id_not_found(self):
        """Test getting a task by non-existent ID."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.get_task_by_id(999)

    def test_update_task(self):
        """Test updating a task."""
        task = self.task_service.add_task("Original Task", "Original Description", "low")
        
        updated_task = self.task_service.update_task(
            task.id,
            title="Updated Task",
            description="Updated Description",
            priority="high",
            completed=True
        )
        
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == "high"
        assert updated_task.completed is True

    def test_update_task_partial(self):
        """Test partially updating a task."""
        task = self.task_service.add_task("Original Task", "Original Description", "low")
        
        updated_task = self.task_service.update_task(task.id, title="New Title")
        
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Unchanged
        assert updated_task.priority == "low"  # Unchanged

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.update_task(999, title="New Title")

    def test_complete_task(self):
        """Test completing a task."""
        task = self.task_service.add_task("Test Task", "Test Description", "medium")
        
        completed_task = self.task_service.complete_task(task.id)
        
        assert completed_task.completed is True

    def test_complete_task_not_found(self):
        """Test completing a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.complete_task(999)

    def test_delete_task(self):
        """Test deleting a task."""
        task = self.task_service.add_task("Test Task", "Test Description", "high")
        
        deleted_task = self.task_service.delete_task(task.id)
        
        assert deleted_task.id == task.id
        assert len(self.task_service.get_all_tasks()) == 0

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.task_service.delete_task(999)

    def test_delete_task_from_multiple(self):
        """Test deleting a task when multiple tasks exist."""
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        task3 = self.task_service.add_task("Task 3", "Description 3", "high")
        
        self.task_service.delete_task(task2.id)
        
        remaining_tasks = self.task_service.get_all_tasks()
        assert len(remaining_tasks) == 2
        assert task1 in remaining_tasks
        assert task3 in remaining_tasks
        assert task2 not in remaining_tasks

    def test_search_tasks(self):
        """Test searching for tasks."""
        self.task_service.add_task("Python Programming", "Learn Python basics", "high")
        self.task_service.add_task("Java Development", "Build Java application", "medium")
        self.task_service.add_task("Python Web Framework", "Learn Django framework", "low")
        
        # Search by title
        python_tasks = self.task_service.search_tasks("Python")
        assert len(python_tasks) == 2
        
        # Search by description
        learn_tasks = self.task_service.search_tasks("Learn")
        assert len(learn_tasks) == 2
        
        # Case insensitive search
        java_tasks = self.task_service.search_tasks("java")
        assert len(java_tasks) == 1

    def test_search_tasks_no_results(self):
        """Test searching for tasks with no matches."""
        self.task_service.add_task("Task 1", "Description 1", "low")
        
        results = self.task_service.search_tasks("nonexistent")
        assert len(results) == 0

    def test_load_tasks_from_file(self):
        """Test loading tasks from an existing file."""
        # Add some tasks
        self.task_service.add_task("Task 1", "Description 1", "low")
        self.task_service.add_task("Task 2", "Description 2", "medium")
        
        # Create a new service instance with the same file
        new_service = TaskService(self.temp_file.name)
        tasks = new_service.get_all_tasks()
        
        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"

    def test_load_tasks_nonexistent_file(self):
        """Test loading tasks when file doesn't exist."""
        nonexistent_file = "/tmp/nonexistent_tasks.json"
        service = TaskService(nonexistent_file)
        
        tasks = service.get_all_tasks()
        assert len(tasks) == 0

    @patch("builtins.open", mock_open(read_data="invalid json"))
    @patch("os.path.exists", return_value=True)
    def test_load_tasks_invalid_json(self):
        """Test loading tasks with invalid JSON."""
        with patch("builtins.print") as mock_print:
            service = TaskService("dummy_file.json")
            tasks = service.get_all_tasks()
            
            assert len(tasks) == 0
            mock_print.assert_called_once()