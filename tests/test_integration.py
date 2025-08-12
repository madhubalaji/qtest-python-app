"""
Integration tests for the task manager application.
"""

import os
import tempfile
import pytest
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskManagerIntegration:
    """Integration tests for the complete task manager workflow."""

    def test_complete_task_lifecycle(self, task_service):
        """Test the complete lifecycle of a task from creation to deletion."""
        # Create a task
        task = task_service.add_task(
            title="Integration Test Task",
            description="This task will go through the complete lifecycle",
            priority="high"
        )
        
        assert task.id == 1
        assert task.title == "Integration Test Task"
        assert task.completed is False
        
        # Verify task exists in the list
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == task.id
        
        # Update the task
        updated_task = task_service.update_task(
            task.id,
            description="Updated description",
            priority="medium"
        )
        
        assert updated_task.description == "Updated description"
        assert updated_task.priority == "medium"
        assert updated_task.title == "Integration Test Task"  # Should remain unchanged
        
        # Complete the task
        completed_task = task_service.complete_task(task.id)
        assert completed_task.completed is True
        
        # Search for the task
        search_results = task_service.search_tasks("Integration")
        assert len(search_results) == 1
        assert search_results[0].id == task.id
        
        # Delete the task
        deleted_task = task_service.delete_task(task.id)
        assert deleted_task.id == task.id
        assert deleted_task.title == "Integration Test Task"
        
        # Verify task is gone
        all_tasks_after_delete = task_service.get_all_tasks()
        assert len(all_tasks_after_delete) == 0
        
        # Verify task cannot be found
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(task.id)

    def test_multiple_tasks_management(self, task_service):
        """Test managing multiple tasks with various operations."""
        # Create multiple tasks
        task1 = task_service.add_task("Task 1", "First task", "high")
        task2 = task_service.add_task("Task 2", "Second task", "medium")
        task3 = task_service.add_task("Task 3", "Third task", "low")
        
        assert len(task_service.get_all_tasks()) == 3
        
        # Complete one task
        task_service.complete_task(task2.id)
        
        # Get only active tasks
        active_tasks = task_service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 2
        
        active_ids = [task.id for task in active_tasks]
        assert task1.id in active_ids
        assert task2.id not in active_ids
        assert task3.id in active_ids
        
        # Delete one task
        task_service.delete_task(task1.id)
        
        # Verify final state
        remaining_tasks = task_service.get_all_tasks()
        assert len(remaining_tasks) == 2
        
        remaining_ids = [task.id for task in remaining_tasks]
        assert task1.id not in remaining_ids
        assert task2.id in remaining_ids
        assert task3.id in remaining_ids

    def test_delete_task_error_handling(self, task_service):
        """Test error handling when deleting non-existent tasks."""
        # Try to delete a task that doesn't exist
        with pytest.raises(TaskNotFoundException) as exc_info:
            task_service.delete_task(999)
        
        assert "Task with ID 999 not found" in str(exc_info.value)
        
        # Create and delete a task, then try to delete it again
        task = task_service.add_task("Test Task")
        task_service.delete_task(task.id)
        
        with pytest.raises(TaskNotFoundException):
            task_service.delete_task(task.id)

    def test_delete_task_persistence_across_sessions(self, temp_storage_file):
        """Test that task deletion persists across different service instances."""
        # Create first service instance and add tasks
        service1 = TaskService(temp_storage_file)
        task1 = service1.add_task("Persistent Task 1")
        task2 = service1.add_task("Persistent Task 2")
        
        # Delete one task
        service1.delete_task(task1.id)
        
        # Create second service instance (simulating app restart)
        service2 = TaskService(temp_storage_file)
        
        # Verify only one task remains
        tasks = service2.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == task2.id
        assert tasks[0].title == "Persistent Task 2"
        
        # Verify deleted task is not found
        with pytest.raises(TaskNotFoundException):
            service2.get_task_by_id(task1.id)

    def test_search_after_delete(self, task_service):
        """Test that search results are updated after task deletion."""
        # Create tasks with searchable content
        task1 = task_service.add_task("Important Meeting", "Discuss project")
        task2 = task_service.add_task("Important Call", "Call client")
        task3 = task_service.add_task("Regular Task", "Do something")
        
        # Search for "Important" tasks
        results = task_service.search_tasks("Important")
        assert len(results) == 2
        
        # Delete one of the important tasks
        task_service.delete_task(task1.id)
        
        # Search again
        results_after_delete = task_service.search_tasks("Important")
        assert len(results_after_delete) == 1
        assert results_after_delete[0].id == task2.id

    def test_delete_completed_task(self, task_service):
        """Test deleting a completed task."""
        # Create and complete a task
        task = task_service.add_task("Task to Complete and Delete")
        task_service.complete_task(task.id)
        
        # Verify task is completed
        completed_task = task_service.get_task_by_id(task.id)
        assert completed_task.completed is True
        
        # Delete the completed task
        deleted_task = task_service.delete_task(task.id)
        assert deleted_task.completed is True
        assert deleted_task.id == task.id
        
        # Verify task is gone
        assert len(task_service.get_all_tasks()) == 0

    def test_delete_task_with_special_characters(self, task_service):
        """Test deleting tasks with special characters in title/description."""
        special_task = task_service.add_task(
            title="Task with émojis 🚀 and spëcial chars!",
            description="Description with 'quotes' and \"double quotes\" & symbols"
        )
        
        # Verify task was created correctly
        retrieved_task = task_service.get_task_by_id(special_task.id)
        assert retrieved_task.title == "Task with émojis 🚀 and spëcial chars!"
        
        # Delete the task
        deleted_task = task_service.delete_task(special_task.id)
        assert deleted_task.title == "Task with émojis 🚀 and spëcial chars!"
        
        # Verify deletion
        assert len(task_service.get_all_tasks()) == 0

    def test_concurrent_operations_simulation(self, task_service):
        """Test simulating concurrent operations that might occur in UI."""
        # Create multiple tasks
        tasks = []
        for i in range(5):
            task = task_service.add_task(f"Task {i+1}", f"Description {i+1}")
            tasks.append(task)
        
        # Simulate various operations that might happen in UI
        # Complete some tasks
        task_service.complete_task(tasks[1].id)
        task_service.complete_task(tasks[3].id)
        
        # Update some tasks
        task_service.update_task(tasks[0].id, priority="high")
        task_service.update_task(tasks[2].id, description="Updated description")
        
        # Delete some tasks
        task_service.delete_task(tasks[1].id)  # Delete a completed task
        task_service.delete_task(tasks[4].id)  # Delete an active task
        
        # Verify final state
        remaining_tasks = task_service.get_all_tasks()
        assert len(remaining_tasks) == 3
        
        # Check specific tasks
        task0 = task_service.get_task_by_id(tasks[0].id)
        assert task0.priority == "high"
        
        task2 = task_service.get_task_by_id(tasks[2].id)
        assert task2.description == "Updated description"
        
        task3 = task_service.get_task_by_id(tasks[3].id)
        assert task3.completed is True
        
        # Verify deleted tasks are gone
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(tasks[1].id)
        
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(tasks[4].id)