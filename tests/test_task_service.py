"""
Tests for the TaskService class.
"""

import pytest
import os
import json
import tempfile
from unittest.mock import patch, mock_open
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
        self.temp_file_path = self.temp_file.name

    def teardown_method(self):
        """Clean up after each test method."""
        # Remove the temporary file
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)

    def test_task_service_initialization_with_empty_file(self):
        """Test TaskService initialization with an empty storage file."""
        service = TaskService(self.temp_file_path)
        assert len(service.tasks) == 0
        assert service.storage_file == self.temp_file_path

    def test_task_service_initialization_with_existing_tasks(self):
        """Test TaskService initialization with existing tasks in storage file."""
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
        with open(self.temp_file_path, 'w') as f:
            json.dump(test_tasks, f)
        
        # Initialize service
        service = TaskService(self.temp_file_path)
        
        assert len(service.tasks) == 2
        assert service.tasks[0].id == 1
        assert service.tasks[0].title == "Test Task 1"
        assert service.tasks[1].id == 2
        assert service.tasks[1].title == "Test Task 2"

    def test_add_task(self):
        """Test adding a new task."""
        service = TaskService(self.temp_file_path)
        
        task = service.add_task("New Task", "Task description", "high")
        
        assert task.id == 1
        assert task.title == "New Task"
        assert task.description == "Task description"
        assert task.priority == "high"
        assert task.completed is False
        assert len(service.tasks) == 1

    def test_add_multiple_tasks_increments_id(self):
        """Test that adding multiple tasks increments the ID correctly."""
        service = TaskService(self.temp_file_path)
        
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert len(service.tasks) == 3

    def test_get_task_by_id_existing(self):
        """Test getting an existing task by ID."""
        service = TaskService(self.temp_file_path)
        added_task = service.add_task("Test Task")
        
        retrieved_task = service.get_task_by_id(added_task.id)
        
        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title

    def test_get_task_by_id_non_existing(self):
        """Test getting a non-existing task by ID raises exception."""
        service = TaskService(self.temp_file_path)
        
        with pytest.raises(TaskNotFoundException):
            service.get_task_by_id(999)

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        service = TaskService(self.temp_file_path)
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")
        
        all_tasks = service.get_all_tasks()
        
        assert len(all_tasks) == 3
        assert all_tasks[0].title == "Task 1"
        assert all_tasks[1].title == "Task 2"
        assert all_tasks[2].title == "Task 3"

    def test_get_active_tasks(self):
        """Test getting only active (non-completed) tasks."""
        service = TaskService(self.temp_file_path)
        task1 = service.add_task("Active Task 1")
        task2 = service.add_task("Completed Task")
        task3 = service.add_task("Active Task 2")
        
        # Mark one task as completed
        service.complete_task(task2.id)
        
        active_tasks = service.get_active_tasks()
        
        assert len(active_tasks) == 2
        assert active_tasks[0].title == "Active Task 1"
        assert active_tasks[1].title == "Active Task 2"
        assert all(not task.completed for task in active_tasks)

    def test_complete_task(self):
        """Test completing a task."""
        service = TaskService(self.temp_file_path)
        task = service.add_task("Task to Complete")
        
        assert task.completed is False
        
        completed_task = service.complete_task(task.id)
        
        assert completed_task.completed is True
        assert service.get_task_by_id(task.id).completed is True

    def test_complete_non_existing_task(self):
        """Test completing a non-existing task raises exception."""
        service = TaskService(self.temp_file_path)
        
        with pytest.raises(TaskNotFoundException):
            service.complete_task(999)

    def test_delete_task(self):
        """Test deleting a task."""
        service = TaskService(self.temp_file_path)
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")
        
        assert len(service.tasks) == 3
        
        service.delete_task(task2.id)
        
        assert len(service.tasks) == 2
        assert service.tasks[0].id == task1.id
        assert service.tasks[1].id == task3.id
        
        with pytest.raises(TaskNotFoundException):
            service.get_task_by_id(task2.id)

    def test_delete_non_existing_task(self):
        """Test deleting a non-existing task raises exception."""
        service = TaskService(self.temp_file_path)
        
        with pytest.raises(TaskNotFoundException):
            service.delete_task(999)

    def test_search_tasks(self):
        """Test searching tasks by keyword."""
        service = TaskService(self.temp_file_path)
        service.add_task("Python Programming", "Learn Python basics")
        service.add_task("Java Development", "Build Java application")
        service.add_task("Python Web App", "Create web app with Python")
        
        # Search for "Python"
        python_tasks = service.search_tasks("Python")
        assert len(python_tasks) == 2
        assert all("Python" in task.title or "Python" in task.description for task in python_tasks)
        
        # Search for "Java"
        java_tasks = service.search_tasks("Java")
        assert len(java_tasks) == 1
        assert "Java" in java_tasks[0].title
        
        # Search for non-existing keyword
        no_tasks = service.search_tasks("NonExisting")
        assert len(no_tasks) == 0

    def test_filter_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        service = TaskService(self.temp_file_path)
        service.add_task("High Priority Task", priority="high")
        service.add_task("Medium Priority Task", priority="medium")
        service.add_task("Low Priority Task", priority="low")
        service.add_task("Another High Priority Task", priority="high")
        
        high_priority_tasks = service.filter_tasks_by_priority("high")
        assert len(high_priority_tasks) == 2
        assert all(task.priority == "high" for task in high_priority_tasks)
        
        medium_priority_tasks = service.filter_tasks_by_priority("medium")
        assert len(medium_priority_tasks) == 1
        assert medium_priority_tasks[0].priority == "medium"

    def test_save_and_load_tasks_persistence(self):
        """Test that tasks are properly saved and loaded from file."""
        # Create service and add tasks
        service1 = TaskService(self.temp_file_path)
        task1 = service1.add_task("Persistent Task 1", "Description 1", "high")
        task2 = service1.add_task("Persistent Task 2", "Description 2", "low")
        
        # Create new service instance with same file
        service2 = TaskService(self.temp_file_path)
        
        # Verify tasks were loaded
        assert len(service2.tasks) == 2
        loaded_task1 = service2.get_task_by_id(task1.id)
        loaded_task2 = service2.get_task_by_id(task2.id)
        
        assert loaded_task1.title == "Persistent Task 1"
        assert loaded_task1.description == "Description 1"
        assert loaded_task1.priority == "high"
        
        assert loaded_task2.title == "Persistent Task 2"
        assert loaded_task2.description == "Description 2"
        assert loaded_task2.priority == "low"

    @patch("builtins.open", mock_open(read_data="invalid json"))
    @patch("os.path.exists", return_value=True)
    def test_load_tasks_with_invalid_json(self):
        """Test loading tasks when JSON file contains invalid data."""
        with patch("builtins.print") as mock_print:
            service = TaskService("dummy_file.json")
            assert len(service.tasks) == 0
            mock_print.assert_called_once_with("Error reading task file. Starting with empty task list.")