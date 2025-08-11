"""
Tests for the Streamlit web application.
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from src.services.task_service import TaskService
from src.models.task import Task


class TestAppFunctionality:
    """Test cases for the web application functionality."""

    @pytest.fixture
    def temp_storage_file(self):
        """Create a temporary storage file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            yield f.name
        # Clean up after test
        if os.path.exists(f.name):
            os.unlink(f.name)

    @pytest.fixture
    def task_service_with_tasks(self, temp_storage_file):
        """Create a TaskService instance with some test tasks."""
        service = TaskService(temp_storage_file)
        service.add_task("Test Task 1", "Description 1", "high")
        service.add_task("Test Task 2", "Description 2", "medium")
        service.add_task("Completed Task", "Description 3", "low")
        service.complete_task(3)  # Mark third task as completed
        return service

    def test_task_service_delete_functionality(self, task_service_with_tasks):
        """Test that the task service delete functionality works correctly."""
        initial_count = len(task_service_with_tasks.get_all_tasks())
        
        # Delete a task
        deleted_task = task_service_with_tasks.delete_task(1)
        
        # Verify task was deleted
        assert deleted_task.title == "Test Task 1"
        assert len(task_service_with_tasks.get_all_tasks()) == initial_count - 1
        
        # Verify the deleted task cannot be found
        with pytest.raises(Exception):  # TaskNotFoundException
            task_service_with_tasks.get_task_by_id(1)

    def test_task_filtering_after_delete(self, task_service_with_tasks):
        """Test that task filtering works correctly after deletion."""
        # Delete an active task
        task_service_with_tasks.delete_task(1)
        
        # Get active tasks (should exclude completed ones)
        active_tasks = task_service_with_tasks.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 1
        assert active_tasks[0].title == "Test Task 2"
        
        # Get all tasks (should include completed ones)
        all_tasks = task_service_with_tasks.get_all_tasks(show_completed=True)
        assert len(all_tasks) == 2

    def test_search_functionality_after_delete(self, task_service_with_tasks):
        """Test that search functionality works correctly after deletion."""
        # Delete a task
        task_service_with_tasks.delete_task(1)
        
        # Search should not find the deleted task
        results = task_service_with_tasks.search_tasks("Test Task 1")
        assert len(results) == 0
        
        # Search should still find remaining tasks
        results = task_service_with_tasks.search_tasks("Test Task 2")
        assert len(results) == 1
        assert results[0].title == "Test Task 2"

    def test_delete_completed_task(self, task_service_with_tasks):
        """Test deleting a completed task."""
        # Delete the completed task
        deleted_task = task_service_with_tasks.delete_task(3)
        
        assert deleted_task.title == "Completed Task"
        assert deleted_task.completed is True
        
        # Verify it's removed from all tasks
        all_tasks = task_service_with_tasks.get_all_tasks(show_completed=True)
        assert len(all_tasks) == 2
        assert all(task.id != 3 for task in all_tasks)

    def test_delete_task_by_priority(self, task_service_with_tasks):
        """Test deleting tasks and verifying priority filtering still works."""
        # Delete the high priority task
        task_service_with_tasks.delete_task(1)
        
        # Get all remaining tasks
        remaining_tasks = task_service_with_tasks.get_all_tasks()
        
        # Filter by priority (simulating web app filtering)
        high_priority_tasks = [task for task in remaining_tasks if task.priority.lower() == "high"]
        medium_priority_tasks = [task for task in remaining_tasks if task.priority.lower() == "medium"]
        low_priority_tasks = [task for task in remaining_tasks if task.priority.lower() == "low"]
        
        assert len(high_priority_tasks) == 0  # High priority task was deleted
        assert len(medium_priority_tasks) == 1
        assert len(low_priority_tasks) == 1

    def test_task_persistence_after_delete(self, temp_storage_file):
        """Test that task deletion is properly persisted to storage."""
        # Create service and add tasks
        service1 = TaskService(temp_storage_file)
        service1.add_task("Task 1", "Description 1")
        service1.add_task("Task 2", "Description 2")
        service1.add_task("Task 3", "Description 3")
        
        # Delete a task
        service1.delete_task(2)
        
        # Create new service instance (simulating app restart)
        service2 = TaskService(temp_storage_file)
        
        # Verify deletion was persisted
        assert len(service2.get_all_tasks()) == 2
        task_ids = [task.id for task in service2.get_all_tasks()]
        assert 2 not in task_ids
        assert 1 in task_ids
        assert 3 in task_ids

    def test_delete_all_tasks(self, task_service_with_tasks):
        """Test deleting all tasks."""
        # Get all task IDs
        all_tasks = task_service_with_tasks.get_all_tasks()
        task_ids = [task.id for task in all_tasks]
        
        # Delete all tasks
        for task_id in task_ids:
            task_service_with_tasks.delete_task(task_id)
        
        # Verify no tasks remain
        remaining_tasks = task_service_with_tasks.get_all_tasks()
        assert len(remaining_tasks) == 0

    def test_delete_and_add_new_task_id_generation(self, task_service_with_tasks):
        """Test that new task IDs are generated correctly after deletions."""
        # Delete some tasks
        task_service_with_tasks.delete_task(1)
        task_service_with_tasks.delete_task(3)
        
        # Add a new task
        new_task = task_service_with_tasks.add_task("New Task", "New Description")
        
        # New task should get the next available ID (4, since max was 3)
        assert new_task.id == 4

    @patch('streamlit.session_state', new_callable=dict)
    def test_session_state_cleanup_simulation(self, mock_session_state):
        """Test session state cleanup logic (simulated)."""
        # Simulate session state with confirmation flags
        mock_session_state['confirm_delete_1'] = True
        mock_session_state['search_confirm_delete_2'] = True
        mock_session_state['detail_confirm_delete_3'] = True
        
        # Simulate cleanup (this would happen in the actual app)
        keys_to_delete = [key for key in mock_session_state.keys() if 'confirm_delete' in key]
        for key in keys_to_delete:
            del mock_session_state[key]
        
        # Verify cleanup
        assert len(mock_session_state) == 0

    def test_task_display_after_delete(self, task_service_with_tasks):
        """Test that task display logic works correctly after deletion."""
        # Delete a task
        task_service_with_tasks.delete_task(2)
        
        # Get tasks for display (simulating the web app logic)
        tasks = task_service_with_tasks.get_all_tasks(show_completed=True)
        
        # Filter out completed tasks (simulating checkbox unchecked)
        active_tasks = [task for task in tasks if not task.completed]
        
        # Should have 1 active task remaining
        assert len(active_tasks) == 1
        assert active_tasks[0].title == "Test Task 1"
        
        # Filter by priority (simulating priority filter)
        high_priority_tasks = [task for task in active_tasks if task.priority.lower() == "high"]
        assert len(high_priority_tasks) == 1