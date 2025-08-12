"""Integration tests for the task manager application."""

import os
import json
import tempfile
import pytest

from src.models.task import Task
from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


class TestIntegration:
    """Integration test cases."""

    @pytest.fixture
    def temp_storage_file(self):
        """Create a temporary storage file for integration tests."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    def test_full_task_lifecycle(self, temp_storage_file):
        """Test complete task lifecycle: create, read, update, delete."""
        service = TaskService(temp_storage_file)
        
        # Create a task
        task = service.add_task("Integration Test Task", "Test Description", "high")
        assert task.id == 1
        assert task.title == "Integration Test Task"
        assert task.completed is False
        
        # Verify task is persisted
        new_service = TaskService(temp_storage_file)
        assert len(new_service.tasks) == 1
        retrieved_task = new_service.get_task_by_id(1)
        assert retrieved_task.title == "Integration Test Task"
        
        # Update the task
        updated_task = new_service.update_task(1, title="Updated Task", completed=True)
        assert updated_task.title == "Updated Task"
        assert updated_task.completed is True
        
        # Verify update is persisted
        another_service = TaskService(temp_storage_file)
        updated_retrieved = another_service.get_task_by_id(1)
        assert updated_retrieved.title == "Updated Task"
        assert updated_retrieved.completed is True
        
        # Delete the task
        deleted_task = another_service.delete_task(1)
        assert deleted_task.id == 1
        
        # Verify deletion is persisted
        final_service = TaskService(temp_storage_file)
        assert len(final_service.tasks) == 0

    def test_multiple_tasks_operations(self, temp_storage_file):
        """Test operations with multiple tasks."""
        service = TaskService(temp_storage_file)
        
        # Add multiple tasks
        task1 = service.add_task("Task 1", "Description 1", "high")
        task2 = service.add_task("Task 2", "Description 2", "medium")
        task3 = service.add_task("Task 3", "Description 3", "low")
        
        assert len(service.tasks) == 3
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        
        # Complete some tasks
        service.complete_task(1)
        service.complete_task(3)
        
        # Test filtering
        active_tasks = service.get_all_tasks(show_completed=False)
        all_tasks = service.get_all_tasks(show_completed=True)
        
        assert len(active_tasks) == 1
        assert len(all_tasks) == 3
        assert active_tasks[0].id == 2
        
        # Test search functionality
        search_results = service.search_tasks("Task")
        assert len(search_results) == 3
        
        specific_search = service.search_tasks("Description 2")
        assert len(specific_search) == 1
        assert specific_search[0].id == 2

    def test_data_persistence_across_instances(self, temp_storage_file):
        """Test that data persists correctly across service instances."""
        # First instance - add data
        service1 = TaskService(temp_storage_file)
        task1 = service1.add_task("Persistent Task", "This should persist", "medium")
        
        # Second instance - should load existing data
        service2 = TaskService(temp_storage_file)
        assert len(service2.tasks) == 1
        loaded_task = service2.get_task_by_id(1)
        assert loaded_task.title == "Persistent Task"
        assert loaded_task.description == "This should persist"
        
        # Modify in second instance
        service2.update_task(1, priority="high")
        
        # Third instance - should see modifications
        service3 = TaskService(temp_storage_file)
        modified_task = service3.get_task_by_id(1)
        assert modified_task.priority == "high"

    def test_json_file_format_compatibility(self, temp_storage_file):
        """Test that the JSON file format is readable and writable."""
        service = TaskService(temp_storage_file)
        
        # Add some tasks
        service.add_task("JSON Test 1", "Description 1", "high")
        service.add_task("JSON Test 2", "Description 2", "low")
        
        # Read the JSON file directly
        with open(temp_storage_file, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 2
        assert data[0]['title'] == "JSON Test 1"
        assert data[0]['priority'] == "high"
        assert data[1]['title'] == "JSON Test 2"
        assert data[1]['priority'] == "low"
        
        # Verify all required fields are present
        required_fields = ['id', 'title', 'description', 'priority', 'completed', 'created_at']
        for task_data in data:
            for field in required_fields:
                assert field in task_data

    def test_error_handling_integration(self, temp_storage_file):
        """Test error handling in integrated scenarios."""
        service = TaskService(temp_storage_file)
        
        # Add a task
        service.add_task("Test Task", "Test Description", "medium")
        
        # Try to operate on non-existent task
        with pytest.raises(Exception):  # Should raise TaskNotFoundException
            service.get_task_by_id(999)
        
        with pytest.raises(Exception):
            service.update_task(999, title="New Title")
        
        with pytest.raises(Exception):
            service.delete_task(999)
        
        # Verify original task is still intact
        original_task = service.get_task_by_id(1)
        assert original_task.title == "Test Task"

    def test_concurrent_access_simulation(self, temp_storage_file):
        """Simulate concurrent access to the same storage file."""
        # This test simulates what might happen if multiple processes
        # access the same file (though not true concurrency)
        
        service1 = TaskService(temp_storage_file)
        service2 = TaskService(temp_storage_file)
        
        # Both services start with empty state
        assert len(service1.tasks) == 0
        assert len(service2.tasks) == 0
        
        # Service1 adds a task
        task1 = service1.add_task("Service1 Task", "From service 1", "high")
        
        # Service2 loads fresh data (simulating another process)
        service2 = TaskService(temp_storage_file)  # Reload from file
        assert len(service2.tasks) == 1
        
        # Service2 adds another task
        task2 = service2.add_task("Service2 Task", "From service 2", "low")
        
        # Create a new service instance to verify both tasks exist
        service3 = TaskService(temp_storage_file)
        assert len(service3.tasks) == 2
        
        titles = [task.title for task in service3.tasks]
        assert "Service1 Task" in titles
        assert "Service2 Task" in titles