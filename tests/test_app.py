"""
Tests for the Streamlit app functionality.
"""

import pytest
import tempfile
import os
import json
from unittest.mock import MagicMock, patch, Mock

from src.models.task import Task
from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


class TestAppFunctionality:
    """Test cases for app functionality."""

    @pytest.fixture
    def temp_storage_file(self):
        """Create a temporary storage file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write('[]')  # Empty task list
            temp_file = f.name
        yield temp_file
        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)

    @pytest.fixture
    def task_service_with_tasks(self, temp_storage_file):
        """Create a TaskService instance with some pre-existing tasks."""
        # Create some initial tasks
        initial_tasks = [
            {"id": 1, "title": "Task 1", "description": "Description 1", "priority": "high", "completed": False, "created_at": "2023-01-01 10:00:00"},
            {"id": 2, "title": "Task 2", "description": "Description 2", "priority": "medium", "completed": False, "created_at": "2023-01-01 11:00:00"},
            {"id": 3, "title": "Task 3", "description": "Description 3", "priority": "low", "completed": True, "created_at": "2023-01-01 12:00:00"}
        ]
        
        with open(temp_storage_file, 'w') as f:
            json.dump(initial_tasks, f)
        
        return TaskService(temp_storage_file)

    def test_task_service_delete_functionality(self, task_service_with_tasks):
        """Test that TaskService delete functionality works correctly."""
        # Verify initial state
        assert len(task_service_with_tasks.tasks) == 3
        
        # Delete a task
        deleted_task = task_service_with_tasks.delete_task(2)
        assert deleted_task.id == 2
        assert len(task_service_with_tasks.tasks) == 2
        
        # Verify task is gone
        with pytest.raises(TaskNotFoundException):
            task_service_with_tasks.get_task_by_id(2)

    def test_delete_and_add_new_task_id_generation(self, task_service_with_tasks):
        """Test that new task IDs are generated correctly after deletions."""
        # Delete some tasks
        task_service_with_tasks.delete_task(1)
        task_service_with_tasks.delete_task(3)
        
        # Add a new task
        new_task = task_service_with_tasks.add_task("New Task", "New Description")
        
        # New task should get the next available ID (4, since max was 3)
        assert new_task.id == 4

    def test_delete_all_tasks_and_add_new(self, task_service_with_tasks):
        """Test deleting all tasks and adding a new one."""
        # Delete all tasks
        task_service_with_tasks.delete_task(1)
        task_service_with_tasks.delete_task(2)
        task_service_with_tasks.delete_task(3)
        
        assert len(task_service_with_tasks.tasks) == 0
        
        # Add a new task
        new_task = task_service_with_tasks.add_task("First New Task")
        
        # Should get ID 4 (continuing from the highest previous ID)
        assert new_task.id == 4

    def test_delete_task_persistence(self, task_service_with_tasks):
        """Test that deleted tasks are persisted to storage."""
        # Delete a task
        task_service_with_tasks.delete_task(1)
        
        # Create new service instance with same storage file
        new_service = TaskService(task_service_with_tasks.storage_file)
        
        # Verify task is still deleted
        assert len(new_service.tasks) == 2
        task_ids = [task.id for task in new_service.tasks]
        assert 1 not in task_ids

    def test_delete_nonexistent_task(self, task_service_with_tasks):
        """Test deleting a task that doesn't exist."""
        with pytest.raises(TaskNotFoundException):
            task_service_with_tasks.delete_task(999)

    def test_delete_task_twice(self, task_service_with_tasks):
        """Test deleting the same task twice."""
        # Delete task once
        task_service_with_tasks.delete_task(1)
        
        # Try to delete again
        with pytest.raises(TaskNotFoundException):
            task_service_with_tasks.delete_task(1)

    def test_complete_and_delete_task(self, task_service_with_tasks):
        """Test completing a task and then deleting it."""
        # Complete a task
        task_service_with_tasks.complete_task(1)
        task = task_service_with_tasks.get_task_by_id(1)
        assert task.completed
        
        # Delete the completed task
        deleted_task = task_service_with_tasks.delete_task(1)
        assert deleted_task.completed
        assert len(task_service_with_tasks.tasks) == 2

    def test_search_and_delete_task(self, task_service_with_tasks):
        """Test searching for a task and then deleting it."""
        # Search for a task
        results = task_service_with_tasks.search_tasks("Task 2")
        assert len(results) == 1
        task_to_delete = results[0]
        
        # Delete the found task
        deleted_task = task_service_with_tasks.delete_task(task_to_delete.id)
        assert deleted_task.id == task_to_delete.id
        
        # Verify it's no longer found in search
        results_after = task_service_with_tasks.search_tasks("Task 2")
        assert len(results_after) == 0

    def test_id_generation_after_multiple_operations(self, task_service_with_tasks):
        """Test ID generation after multiple add/delete operations."""
        # Initial state: tasks 1, 2, 3 exist
        assert task_service_with_tasks._next_id == 4
        
        # Add a task (should get ID 4)
        task4 = task_service_with_tasks.add_task("Task 4")
        assert task4.id == 4
        assert task_service_with_tasks._next_id == 5
        
        # Delete some tasks
        task_service_with_tasks.delete_task(2)
        task_service_with_tasks.delete_task(4)
        
        # Add another task (should get ID 5, not reuse 2 or 4)
        task5 = task_service_with_tasks.add_task("Task 5")
        assert task5.id == 5
        assert task_service_with_tasks._next_id == 6

    def test_task_service_initialization_with_gaps(self):
        """Test TaskService initialization when storage has gaps in IDs."""
        # Create storage with gaps in IDs
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            tasks_with_gaps = [
                {"id": 1, "title": "Task 1", "description": "", "priority": "medium", "completed": False, "created_at": "2023-01-01 10:00:00"},
                {"id": 5, "title": "Task 5", "description": "", "priority": "medium", "completed": False, "created_at": "2023-01-01 11:00:00"},
                {"id": 10, "title": "Task 10", "description": "", "priority": "medium", "completed": False, "created_at": "2023-01-01 12:00:00"}
            ]
            json.dump(tasks_with_gaps, f)
            temp_file = f.name
        
        try:
            # Initialize service
            service = TaskService(temp_file)
            
            # Next ID should be 11 (max existing ID + 1)
            assert service._next_id == 11
            
            # Add a new task
            new_task = service.add_task("New Task")
            assert new_task.id == 11
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    @patch('streamlit.button')
    @patch('streamlit.experimental_rerun')
    def test_delete_button_functionality(self, mock_rerun, mock_button):
        """Test that delete buttons work correctly in the UI."""
        # This is a simplified test for the delete button logic
        # In a real scenario, you'd need more sophisticated Streamlit mocking
        
        # Mock button to return True (simulating click)
        mock_button.return_value = True
        
        # Create a task service with tasks
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            initial_tasks = [
                {"id": 1, "title": "Task 1", "description": "Description 1", "priority": "high", "completed": False, "created_at": "2023-01-01 10:00:00"}
            ]
            json.dump(initial_tasks, f)
            temp_file = f.name
        
        try:
            task_service = TaskService(temp_file)
            initial_count = len(task_service.tasks)
            
            # Simulate delete operation (this would normally be triggered by UI)
            task_service.delete_task(1)
            
            # Verify task was deleted
            assert len(task_service.tasks) == initial_count - 1
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_empty_task_list_operations(self):
        """Test operations on empty task list."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write('[]')
            temp_file = f.name
        
        try:
            service = TaskService(temp_file)
            
            # Verify empty state
            assert len(service.tasks) == 0
            assert service._next_id == 1
            
            # Try to delete from empty list
            with pytest.raises(TaskNotFoundException):
                service.delete_task(1)
            
            # Add first task
            task = service.add_task("First Task")
            assert task.id == 1
            assert len(service.tasks) == 1
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)