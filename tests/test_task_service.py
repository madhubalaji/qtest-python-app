"""
Unit tests for the TaskService class.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test cases for the TaskService class."""

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    @pytest.fixture
    def sample_tasks_data(self):
        """Sample task data for testing."""
        return [
            {
                "id": 1,
                "title": "Task 1",
                "description": "Description 1",
                "priority": "high",
                "completed": False,
                "created_at": "2023-01-01 12:00:00"
            },
            {
                "id": 2,
                "title": "Task 2",
                "description": "Description 2",
                "priority": "medium",
                "completed": True,
                "created_at": "2023-01-02 12:00:00"
            }
        ]

    @pytest.fixture
    def task_service_with_data(self, temp_file, sample_tasks_data):
        """Create a TaskService with sample data."""
        with open(temp_file, 'w') as f:
            json.dump(sample_tasks_data, f)
        return TaskService(temp_file)

    def test_init_with_nonexistent_file(self, temp_file):
        """Test initializing TaskService with non-existent file."""
        # Remove the temp file to simulate non-existent file
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        
        service = TaskService(temp_file)
        assert service.storage_file == temp_file
        assert len(service.tasks) == 0

    def test_init_with_existing_file(self, task_service_with_data):
        """Test initializing TaskService with existing file."""
        service = task_service_with_data
        assert len(service.tasks) == 2
        assert service.tasks[0].id == 1
        assert service.tasks[0].title == "Task 1"
        assert service.tasks[1].id == 2
        assert service.tasks[1].title == "Task 2"

    def test_init_with_invalid_json(self, temp_file):
        """Test initializing TaskService with invalid JSON file."""
        with open(temp_file, 'w') as f:
            f.write("invalid json content")
        
        with patch('builtins.print') as mock_print:
            service = TaskService(temp_file)
            assert len(service.tasks) == 0
            mock_print.assert_called_once_with("Error reading task file. Starting with empty task list.")

    def test_add_task_to_empty_service(self, temp_file):
        """Test adding a task to empty service."""
        service = TaskService(temp_file)
        task = service.add_task("New Task", "New Description", "high")
        
        assert task.id == 1
        assert task.title == "New Task"
        assert task.description == "New Description"
        assert task.priority == "high"
        assert task.completed is False
        assert len(service.tasks) == 1

    def test_add_task_with_existing_tasks(self, task_service_with_data):
        """Test adding a task when tasks already exist."""
        service = task_service_with_data
        initial_count = len(service.tasks)
        
        task = service.add_task("New Task", "New Description", "low")
        
        assert task.id == 3  # Should be max existing ID + 1
        assert task.title == "New Task"
        assert len(service.tasks) == initial_count + 1

    def test_add_task_with_defaults(self, temp_file):
        """Test adding a task with default values."""
        service = TaskService(temp_file)
        task = service.add_task("Task Title")
        
        assert task.title == "Task Title"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False

    def test_get_all_tasks_show_completed(self, task_service_with_data):
        """Test getting all tasks including completed ones."""
        service = task_service_with_data
        tasks = service.get_all_tasks(show_completed=True)
        
        assert len(tasks) == 2
        assert any(task.completed for task in tasks)

    def test_get_all_tasks_hide_completed(self, task_service_with_data):
        """Test getting all tasks excluding completed ones."""
        service = task_service_with_data
        tasks = service.get_all_tasks(show_completed=False)
        
        assert len(tasks) == 1
        assert not any(task.completed for task in tasks)

    def test_get_task_by_id_existing(self, task_service_with_data):
        """Test getting an existing task by ID."""
        service = task_service_with_data
        task = service.get_task_by_id(1)
        
        assert task.id == 1
        assert task.title == "Task 1"

    def test_get_task_by_id_nonexistent(self, task_service_with_data):
        """Test getting a non-existent task by ID."""
        service = task_service_with_data
        
        with pytest.raises(TaskNotFoundException) as exc_info:
            service.get_task_by_id(999)
        
        assert "Task with ID 999 not found" in str(exc_info.value)

    def test_update_task_title(self, task_service_with_data):
        """Test updating task title."""
        service = task_service_with_data
        updated_task = service.update_task(1, title="Updated Title")
        
        assert updated_task.title == "Updated Title"
        assert updated_task.id == 1

    def test_update_task_multiple_fields(self, task_service_with_data):
        """Test updating multiple task fields."""
        service = task_service_with_data
        updated_task = service.update_task(
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

    def test_update_nonexistent_task(self, task_service_with_data):
        """Test updating a non-existent task."""
        service = task_service_with_data
        
        with pytest.raises(TaskNotFoundException):
            service.update_task(999, title="New Title")

    def test_complete_task(self, task_service_with_data):
        """Test marking a task as complete."""
        service = task_service_with_data
        completed_task = service.complete_task(1)
        
        assert completed_task.completed is True
        assert completed_task.id == 1

    def test_complete_nonexistent_task(self, task_service_with_data):
        """Test completing a non-existent task."""
        service = task_service_with_data
        
        with pytest.raises(TaskNotFoundException):
            service.complete_task(999)

    def test_delete_task_existing(self, task_service_with_data):
        """Test deleting an existing task."""
        service = task_service_with_data
        initial_count = len(service.tasks)
        
        deleted_task = service.delete_task(1)
        
        assert deleted_task.id == 1
        assert len(service.tasks) == initial_count - 1
        
        # Verify task is actually removed
        with pytest.raises(TaskNotFoundException):
            service.get_task_by_id(1)

    def test_delete_nonexistent_task(self, task_service_with_data):
        """Test deleting a non-existent task."""
        service = task_service_with_data
        
        with pytest.raises(TaskNotFoundException):
            service.delete_task(999)

    def test_search_tasks_by_title(self, task_service_with_data):
        """Test searching tasks by title."""
        service = task_service_with_data
        results = service.search_tasks("Task 1")
        
        assert len(results) == 1
        assert results[0].title == "Task 1"

    def test_search_tasks_by_description(self, task_service_with_data):
        """Test searching tasks by description."""
        service = task_service_with_data
        results = service.search_tasks("Description 2")
        
        assert len(results) == 1
        assert results[0].description == "Description 2"

    def test_search_tasks_case_insensitive(self, task_service_with_data):
        """Test that search is case insensitive."""
        service = task_service_with_data
        results = service.search_tasks("TASK 1")
        
        assert len(results) == 1
        assert results[0].title == "Task 1"

    def test_search_tasks_partial_match(self, task_service_with_data):
        """Test searching with partial matches."""
        service = task_service_with_data
        results = service.search_tasks("Task")
        
        assert len(results) == 2  # Should match both tasks

    def test_search_tasks_no_results(self, task_service_with_data):
        """Test searching with no matching results."""
        service = task_service_with_data
        results = service.search_tasks("nonexistent")
        
        assert len(results) == 0

    def test_save_tasks_persistence(self, temp_file):
        """Test that tasks are properly saved to file."""
        service = TaskService(temp_file)
        service.add_task("Test Task", "Test Description", "high")
        
        # Create a new service instance to verify persistence
        new_service = TaskService(temp_file)
        assert len(new_service.tasks) == 1
        assert new_service.tasks[0].title == "Test Task"

    def test_file_operations_with_mock(self):
        """Test file operations with mocked file system."""
        mock_data = json.dumps([{
            "id": 1,
            "title": "Mock Task",
            "description": "Mock Description",
            "priority": "medium",
            "completed": False,
            "created_at": "2023-01-01 12:00:00"
        }])
        
        with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
            with patch("os.path.exists", return_value=True):
                service = TaskService("mock_file.json")
                
                assert len(service.tasks) == 1
                assert service.tasks[0].title == "Mock Task"
                mock_file.assert_called_with("mock_file.json", "r")

    @pytest.mark.parametrize("priority", ["low", "medium", "high"])
    def test_add_task_different_priorities(self, temp_file, priority):
        """Test adding tasks with different priorities."""
        service = TaskService(temp_file)
        task = service.add_task("Test Task", priority=priority)
        assert task.priority == priority

    def test_task_id_generation_sequence(self, temp_file):
        """Test that task IDs are generated in sequence."""
        service = TaskService(temp_file)
        
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3