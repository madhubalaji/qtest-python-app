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
        self.service = TaskService(storage_file=self.temp_file.name)

    def teardown_method(self):
        """Clean up after each test method."""
        # Remove the temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_init_with_nonexistent_file(self):
        """Test initialization with a non-existent storage file."""
        non_existent_file = "non_existent_file.json"
        service = TaskService(storage_file=non_existent_file)
        
        assert service.storage_file == non_existent_file
        assert service.tasks == []

    def test_init_with_existing_file(self):
        """Test initialization with an existing storage file."""
        # Create test data
        test_tasks = [
            {
                "id": 1,
                "title": "Test Task 1",
                "description": "Description 1",
                "priority": "high",
                "completed": False,
                "created_at": "2023-01-01 10:00:00"
            },
            {
                "id": 2,
                "title": "Test Task 2",
                "description": "Description 2",
                "priority": "low",
                "completed": True,
                "created_at": "2023-01-01 11:00:00"
            }
        ]
        
        # Write test data to file
        with open(self.temp_file.name, 'w') as f:
            json.dump(test_tasks, f)
        
        # Initialize service
        service = TaskService(storage_file=self.temp_file.name)
        
        assert len(service.tasks) == 2
        assert service.tasks[0].id == 1
        assert service.tasks[0].title == "Test Task 1"
        assert service.tasks[1].id == 2
        assert service.tasks[1].title == "Test Task 2"

    def test_init_with_corrupted_file(self):
        """Test initialization with a corrupted JSON file."""
        # Write invalid JSON to file
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json content")
        
        # Should handle the error gracefully
        with patch('builtins.print') as mock_print:
            service = TaskService(storage_file=self.temp_file.name)
            mock_print.assert_called_once_with("Error reading task file. Starting with empty task list.")
            assert service.tasks == []

    def test_add_task_basic(self):
        """Test adding a basic task."""
        task = self.service.add_task("New Task")
        
        assert task.id == 1
        assert task.title == "New Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False
        assert len(self.service.tasks) == 1

    def test_add_task_with_all_parameters(self):
        """Test adding a task with all parameters."""
        task = self.service.add_task(
            title="Important Task",
            description="This is important",
            priority="high"
        )
        
        assert task.id == 1
        assert task.title == "Important Task"
        assert task.description == "This is important"
        assert task.priority == "high"
        assert task.completed is False

    def test_add_multiple_tasks_id_increment(self):
        """Test that task IDs increment correctly."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert len(self.service.tasks) == 3

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when list is empty."""
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
        """Test updating a task's title."""
        task = self.service.add_task("Original Title")
        updated_task = self.service.update_task(task.id, title="Updated Title")
        
        assert updated_task.title == "Updated Title"
        assert updated_task.id == task.id

    def test_update_task_multiple_fields(self):
        """Test updating multiple fields of a task."""
        task = self.service.add_task("Original Task")
        updated_task = self.service.update_task(
            task.id,
            title="Updated Title",
            description="Updated Description",
            priority="high",
            completed=True
        )
        
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == "high"
        assert updated_task.completed is True

    def test_update_task_nonexistent(self):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.service.update_task(999, title="New Title")

    def test_complete_task(self):
        """Test marking a task as complete."""
        task = self.service.add_task("Task to Complete")
        completed_task = self.service.complete_task(task.id)
        
        assert completed_task.completed is True
        assert completed_task.id == task.id

    def test_complete_task_nonexistent(self):
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
        
        # Verify task is actually removed
        with pytest.raises(TaskNotFoundException):
            self.service.get_task_by_id(task.id)

    def test_delete_task_nonexistent(self):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            self.service.delete_task(999)

    def test_search_tasks_by_title(self):
        """Test searching tasks by title."""
        self.service.add_task("Important Meeting")
        self.service.add_task("Buy Groceries")
        self.service.add_task("Important Call")
        
        results = self.service.search_tasks("important")
        
        assert len(results) == 2
        assert all("important" in task.title.lower() for task in results)

    def test_search_tasks_by_description(self):
        """Test searching tasks by description."""
        self.service.add_task("Task 1", description="This is urgent work")
        self.service.add_task("Task 2", description="Regular maintenance")
        self.service.add_task("Task 3", description="Urgent bug fix")
        
        results = self.service.search_tasks("urgent")
        
        assert len(results) == 2
        assert all("urgent" in task.description.lower() for task in results)

    def test_search_tasks_case_insensitive(self):
        """Test that search is case insensitive."""
        self.service.add_task("UPPERCASE TASK")
        self.service.add_task("lowercase task")
        self.service.add_task("MiXeD cAsE tAsK")
        
        results = self.service.search_tasks("TASK")
        
        assert len(results) == 3

    def test_search_tasks_no_results(self):
        """Test searching with no matching results."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        
        results = self.service.search_tasks("nonexistent")
        
        assert results == []

    def test_search_tasks_empty_keyword(self):
        """Test searching with empty keyword."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        
        results = self.service.search_tasks("")
        
        # Empty string should match all tasks
        assert len(results) == 2

    def test_save_and_load_persistence(self):
        """Test that tasks are properly saved and loaded."""
        # Add tasks
        task1 = self.service.add_task("Persistent Task 1", "Description 1", "high")
        task2 = self.service.add_task("Persistent Task 2", "Description 2", "low")
        
        # Create new service instance with same file
        new_service = TaskService(storage_file=self.temp_file.name)
        
        # Verify tasks were loaded
        assert len(new_service.tasks) == 2
        
        loaded_task1 = new_service.get_task_by_id(task1.id)
        loaded_task2 = new_service.get_task_by_id(task2.id)
        
        assert loaded_task1.title == "Persistent Task 1"
        assert loaded_task1.description == "Description 1"
        assert loaded_task1.priority == "high"
        
        assert loaded_task2.title == "Persistent Task 2"
        assert loaded_task2.description == "Description 2"
        assert loaded_task2.priority == "low"

    def test_task_id_generation_with_existing_tasks(self):
        """Test that new task IDs are generated correctly when tasks already exist."""
        # Pre-populate with tasks
        test_tasks = [
            {"id": 5, "title": "Task 5", "description": "", "priority": "medium", "completed": False, "created_at": "2023-01-01 10:00:00"},
            {"id": 10, "title": "Task 10", "description": "", "priority": "medium", "completed": False, "created_at": "2023-01-01 11:00:00"}
        ]
        
        with open(self.temp_file.name, 'w') as f:
            json.dump(test_tasks, f)
        
        service = TaskService(storage_file=self.temp_file.name)
        new_task = service.add_task("New Task")
        
        # Should get ID 11 (max existing ID + 1)
        assert new_task.id == 11