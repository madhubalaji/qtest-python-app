"""
Integration tests for the task manager application.
"""

import pytest
import tempfile
import os
from src.services.task_service import TaskService
from src.models.task import Task


class TestTaskManagerIntegration:
    """Integration tests for the complete task management workflow."""

    @pytest.fixture
    def temp_storage_file(self):
        """Create a temporary file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        yield temp_file
        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)

    def test_complete_task_workflow(self, temp_storage_file):
        """Test a complete task management workflow."""
        # Initialize service
        service = TaskService(storage_file=temp_storage_file)
        
        # Add tasks
        task1 = service.add_task("Buy groceries", "Milk, bread, eggs", "high")
        task2 = service.add_task("Write report", "Quarterly sales report", "medium")
        task3 = service.add_task("Call dentist", "", "low")
        
        # Verify tasks were added
        assert len(service.get_all_tasks()) == 3
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        
        # Search for tasks
        grocery_tasks = service.search_tasks("groceries")
        assert len(grocery_tasks) == 1
        assert grocery_tasks[0].title == "Buy groceries"
        
        # Complete a task
        completed_task = service.complete_task(1)
        assert completed_task.completed is True
        
        # Get active tasks only
        active_tasks = service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 2
        
        # Update a task
        updated_task = service.update_task(2, priority="high", description="Updated description")
        assert updated_task.priority == "high"
        assert updated_task.description == "Updated description"
        
        # Delete a task
        deleted_task = service.delete_task(3)
        assert deleted_task.title == "Call dentist"
        assert len(service.get_all_tasks()) == 2
        
        # Verify persistence by creating new service instance
        new_service = TaskService(storage_file=temp_storage_file)
        assert len(new_service.get_all_tasks()) == 2
        
        # Verify the completed task is still marked as completed
        task_1_reloaded = new_service.get_task_by_id(1)
        assert task_1_reloaded.completed is True
        
        # Verify the updated task retained its changes
        task_2_reloaded = new_service.get_task_by_id(2)
        assert task_2_reloaded.priority == "high"
        assert task_2_reloaded.description == "Updated description"

    def test_task_model_integration(self):
        """Test Task model integration with dictionary conversion."""
        # Create a task
        original_task = Task(
            task_id=100,
            title="Integration Test Task",
            description="Testing model integration",
            priority="high",
            completed=False
        )
        
        # Convert to dict and back
        task_dict = original_task.to_dict()
        reconstructed_task = Task.from_dict(task_dict)
        
        # Verify all properties are preserved
        assert reconstructed_task.id == original_task.id
        assert reconstructed_task.title == original_task.title
        assert reconstructed_task.description == original_task.description
        assert reconstructed_task.priority == original_task.priority
        assert reconstructed_task.completed == original_task.completed
        assert reconstructed_task.created_at == original_task.created_at

    def test_error_handling_integration(self, temp_storage_file):
        """Test error handling in integrated scenarios."""
        service = TaskService(storage_file=temp_storage_file)
        
        # Add a task
        service.add_task("Test Task")
        
        # Try to access non-existent task
        with pytest.raises(Exception):  # Should be TaskNotFoundException
            service.get_task_by_id(999)
        
        # Try to update non-existent task
        with pytest.raises(Exception):  # Should be TaskNotFoundException
            service.update_task(999, title="Updated")
        
        # Try to complete non-existent task
        with pytest.raises(Exception):  # Should be TaskNotFoundException
            service.complete_task(999)
        
        # Try to delete non-existent task
        with pytest.raises(Exception):  # Should be TaskNotFoundException
            service.delete_task(999)