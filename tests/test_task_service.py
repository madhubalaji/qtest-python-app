"""
Unit tests for the TaskService class.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test cases for the TaskService class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Use a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.service = TaskService(storage_file=self.temp_file.name)

    def teardown_method(self):
        """Clean up after each test method."""
        # Remove the temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_init_with_existing_file(self):
        """Test TaskService initialization with existing file."""
        # Create test data
        test_tasks = [
            {
                "id": 1,
                "title": "Test Task 1",
                "description": "Description 1",
                "priority": "high",
                "completed": False,
                "created_at": "2023-01-01 12:00:00"
            },
            {
                "id": 2,
                "title": "Test Task 2",
                "description": "Description 2",
                "priority": "low",
                "completed": True,
                "created_at": "2023-01-02 12:00:00"
            }
        ]
        
        # Write test data to file
        with open(self.temp_file.name, 'w') as f:
            json.dump(test_tasks, f)
        
        # Initialize service
        service = TaskService(storage_file=self.temp_file.name)
        
        # Verify tasks were loaded
        assert len(service.tasks) == 2
        assert service.tasks[0].id == 1
        assert service.tasks[0].title == "Test Task 1"
        assert service.tasks[1].id == 2
        assert service.tasks[1].completed is True

    def test_init_with_nonexistent_file(self):
        """Test TaskService initialization with non-existent file."""
        non_existent_file = "/tmp/non_existent_file.json"
        service = TaskService(storage_file=non_existent_file)
        
        assert len(service.tasks) == 0
        assert service.storage_file == non_existent_file

    @patch('builtins.open', mock_open(read_data='invalid json'))
    @patch('builtins.print')
    def test_init_with_invalid_json(self, mock_print):
        """Test TaskService initialization with invalid JSON file."""
        with patch('os.path.exists', return_value=True):
            service = TaskService(storage_file="invalid.json")
            
            assert len(service.tasks) == 0
            mock_print.assert_called_once_with("Error reading task file. Starting with empty task list.")

    def test_add_task_to_empty_service(self):
        """Test adding a task to an empty service."""
        task = self.service.add_task("New Task", "Task description", "high")
        
        assert task.id == 1
        assert task.title == "New Task"
        assert task.description == "Task description"
        assert task.priority == "high"
        assert task.completed is False
        assert len(self.service.tasks) == 1

    def test_add_task_with_defaults(self):
        """Test adding a task with default values."""
        task = self.service.add_task("Simple Task")
        
        assert task.id == 1
        assert task.title == "Simple Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks and ID increment."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert len(self.service.tasks) == 3

    def test_get_all_tasks_empty(self):
        """Test getting all tasks from empty service."""
        tasks = self.service.get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_with_completed(self):
        """Test getting all tasks including completed ones."""
        self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task2.completed = True
        
        tasks = self.service.get_all_tasks(show_completed=True)
        assert len(tasks) == 2

    def test_get_all_tasks_without_completed(self):
        """Test getting all tasks excluding completed ones."""
        self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task2.completed = True
        
        tasks = self.service.get_all_tasks(show_completed=False)
        assert len(tasks) == 1
        assert tasks[0].title == "Task 1"

    def test_get_task_by_id_existing(self):
        """Test getting an existing task by ID."""
        added_task = self.service.add_task("Test Task")
        retrieved_task = self.service.get_task_by_id(added_task.id)
        
        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title

    def test_get_task_by_id_nonexistent(self):
        """Test getting a non-existent task by ID."""
        with pytest.raises(TaskNotFoundException) as exc_info:
            self.service.get_task_by_id(999)
        
        assert "Task with ID 999 not found" in str(exc_info.value)

    def test_update_task_title(self):
        """Test updating task title."""
        task = self.service.add_task("Original Title")
        updated_task = self.service.update_task(task.id, title="Updated Title")
        
        assert updated_task.title == "Updated Title"
        assert updated_task.id == task.id

    def test_update_task_multiple_fields(self):
        """Test updating multiple task fields."""
        task = self.service.add_task("Original Task")
        updated_task = self.service.update_task(
            task.id,
            title="New Title",
            description="New Description",
            priority="high",
            completed=True
        )
        
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.priority == "high"
        assert updated_task.completed is True

    def test_update_nonexistent_task(self):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.service.update_task(999, title="New Title")

    def test_complete_task(self):
        """Test marking a task as complete."""
        task = self.service.add_task("Task to Complete")
        completed_task = self.service.complete_task(task.id)
        
        assert completed_task.completed is True
        assert completed_task.id == task.id

    def test_complete_nonexistent_task(self):
        """Test completing a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.service.complete_task(999)

    def test_delete_task(self):
        """Test deleting a task."""
        task = self.service.add_task("Task to Delete")
        initial_count = len(self.service.tasks)
        
        deleted_task = self.service.delete_task(task.id)
        
        assert deleted_task.id == task.id
        assert len(self.service.tasks) == initial_count - 1
        
        with pytest.raises(TaskNotFoundException):
            self.service.get_task_by_id(task.id)

    def test_delete_nonexistent_task(self):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.service.delete_task(999)

    def test_search_tasks_by_title(self):
        """Test searching tasks by title."""
        self.service.add_task("Python Programming")
        self.service.add_task("Java Development")
        self.service.add_task("Python Testing")
        
        results = self.service.search_tasks("python")
        
        assert len(results) == 2
        assert all("python" in task.title.lower() for task in results)

    def test_search_tasks_by_description(self):
        """Test searching tasks by description."""
        self.service.add_task("Task 1", "Learn Python programming")
        self.service.add_task("Task 2", "Study Java concepts")
        self.service.add_task("Task 3", "Python web development")
        
        results = self.service.search_tasks("python")
        
        assert len(results) == 2

    def test_search_tasks_case_insensitive(self):
        """Test that search is case insensitive."""
        self.service.add_task("PYTHON Task")
        self.service.add_task("python task")
        self.service.add_task("Python Task")
        
        results = self.service.search_tasks("PYTHON")
        assert len(results) == 3
        
        results = self.service.search_tasks("python")
        assert len(results) == 3
        
        results = self.service.search_tasks("Python")
        assert len(results) == 3

    def test_search_tasks_no_results(self):
        """Test searching with no matching results."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        
        results = self.service.search_tasks("nonexistent")
        assert len(results) == 0

    def test_search_tasks_empty_keyword(self):
        """Test searching with empty keyword."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        
        results = self.service.search_tasks("")
        assert len(results) == 2  # Empty string matches all tasks

    def test_save_tasks_persistence(self):
        """Test that tasks are persisted to file."""
        # Add tasks
        self.service.add_task("Persistent Task 1")
        self.service.add_task("Persistent Task 2")
        
        # Create new service instance with same file
        new_service = TaskService(storage_file=self.temp_file.name)
        
        # Verify tasks were loaded
        assert len(new_service.tasks) == 2
        assert new_service.tasks[0].title == "Persistent Task 1"
        assert new_service.tasks[1].title == "Persistent Task 2"

    def test_file_operations_integration(self):
        """Test complete file operations integration."""
        # Add initial tasks
        task1 = self.service.add_task("Task 1", "Description 1", "high")
        task2 = self.service.add_task("Task 2", "Description 2", "low")
        
        # Update a task
        self.service.update_task(task1.id, title="Updated Task 1", completed=True)
        
        # Delete a task
        self.service.delete_task(task2.id)
        
        # Add another task
        task3 = self.service.add_task("Task 3", "Description 3", "medium")
        
        # Create new service instance to verify persistence
        new_service = TaskService(storage_file=self.temp_file.name)
        
        # Verify final state
        assert len(new_service.tasks) == 2
        
        # Find the updated task
        updated_task = new_service.get_task_by_id(task1.id)
        assert updated_task.title == "Updated Task 1"
        assert updated_task.completed is True
        
        # Verify task3 exists
        task3_loaded = new_service.get_task_by_id(task3.id)
        assert task3_loaded.title == "Task 3"
        
        # Verify task2 was deleted
        with pytest.raises(TaskNotFoundException):
            new_service.get_task_by_id(task2.id)

    def test_concurrent_access_simulation(self):
        """Test behavior with multiple service instances."""
        # Add task with first service
        task1 = self.service.add_task("Task from Service 1")
        
        # Create second service instance
        service2 = TaskService(storage_file=self.temp_file.name)
        
        # Add task with second service
        task2 = service2.add_task("Task from Service 2")
        
        # Verify both services have their respective tasks
        assert len(self.service.tasks) == 1
        assert len(service2.tasks) == 2  # Loaded existing + added new
        
        # Verify task IDs are handled correctly
        assert task1.id == 1
        assert task2.id == 2

    def test_edge_case_empty_title(self):
        """Test adding task with empty title."""
        task = self.service.add_task("")
        
        assert task.title == ""
        assert task.id == 1
        assert len(self.service.tasks) == 1

    def test_edge_case_very_long_content(self):
        """Test adding task with very long title and description."""
        long_title = "A" * 1000
        long_description = "B" * 5000
        
        task = self.service.add_task(long_title, long_description)
        
        assert task.title == long_title
        assert task.description == long_description
        
        # Verify persistence of long content
        new_service = TaskService(storage_file=self.temp_file.name)
        loaded_task = new_service.get_task_by_id(task.id)
        
        assert loaded_task.title == long_title
        assert loaded_task.description == long_description

    def test_special_characters_in_content(self):
        """Test tasks with special characters."""
        special_title = "Task with émojis 🚀 and spëcial chars: @#$%^&*()"
        special_description = "Description with newlines\nand tabs\t and unicode: ñáéíóú"
        
        task = self.service.add_task(special_title, special_description)
        
        # Verify persistence of special characters
        new_service = TaskService(storage_file=self.temp_file.name)
        loaded_task = new_service.get_task_by_id(task.id)
        
        assert loaded_task.title == special_title
        assert loaded_task.description == special_description

    def test_task_id_generation_with_existing_tasks(self):
        """Test that task ID generation works correctly with pre-existing tasks."""
        # Create initial tasks with specific IDs
        initial_tasks = [
            {
                "id": 5,
                "title": "Existing Task 1",
                "description": "",
                "priority": "medium",
                "completed": False,
                "created_at": "2023-01-01 12:00:00"
            },
            {
                "id": 10,
                "title": "Existing Task 2",
                "description": "",
                "priority": "medium",
                "completed": False,
                "created_at": "2023-01-01 12:00:00"
            }
        ]
        
        # Write to file
        with open(self.temp_file.name, 'w') as f:
            json.dump(initial_tasks, f)
        
        # Create service and add new task
        service = TaskService(storage_file=self.temp_file.name)
        new_task = service.add_task("New Task")
        
        # Verify new task gets ID 11 (max existing ID + 1)
        assert new_task.id == 11

    def test_update_task_partial_fields(self):
        """Test updating only some fields of a task."""
        task = self.service.add_task("Original", "Original desc", "low")
        
        # Update only title
        self.service.update_task(task.id, title="New Title")
        updated_task = self.service.get_task_by_id(task.id)
        
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original desc"  # unchanged
        assert updated_task.priority == "low"  # unchanged
        assert updated_task.completed is False  # unchanged

    def test_search_partial_matches(self):
        """Test search with partial keyword matches."""
        self.service.add_task("Programming in Python")
        self.service.add_task("Java Programming")
        self.service.add_task("Web Development")
        
        # Search for partial match
        results = self.service.search_tasks("prog")
        assert len(results) == 2
        
        # Search for another partial match
        results = self.service.search_tasks("dev")
        assert len(results) == 1
        assert results[0].title == "Web Development"

    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_save_tasks_permission_error(self, mock_open):
        """Test handling of permission errors during save."""
        with pytest.raises(PermissionError):
            self.service.add_task("Test Task")

    def test_service_with_default_storage_file(self):
        """Test TaskService with default storage file name."""
        service = TaskService()  # Uses default "tasks.json"
        
        assert service.storage_file == "tasks.json"
        assert len(service.tasks) == 0
        
        # Clean up if default file was created
        if os.path.exists("tasks.json"):
            os.unlink("tasks.json")