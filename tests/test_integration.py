"""
Integration tests for the task manager application.
"""

import pytest
import tempfile
import os
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskManagerIntegration:
    """Integration tests for the complete task management workflow."""

    @pytest.fixture
    def temp_storage_file(self):
        """Create a temporary storage file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        yield temp_file
        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)

    @pytest.fixture
    def task_service(self, temp_storage_file):
        """Create a TaskService instance with temporary storage."""
        return TaskService(temp_storage_file)

    def test_complete_task_lifecycle(self, task_service):
        """Test the complete lifecycle of a task: create, read, update, delete."""
        # Create task
        task = task_service.add_task(
            title="Integration Test Task",
            description="Testing complete lifecycle",
            priority="high"
        )
        
        assert task.id == 1
        assert task.title == "Integration Test Task"
        assert task.completed is False
        
        # Read task
        retrieved_task = task_service.get_task_by_id(task.id)
        assert retrieved_task.title == task.title
        assert retrieved_task.description == task.description
        
        # Update task
        updated_task = task_service.update_task(
            task.id,
            title="Updated Task Title",
            description="Updated description"
        )
        assert updated_task.title == "Updated Task Title"
        assert updated_task.description == "Updated description"
        
        # Complete task
        completed_task = task_service.complete_task(task.id)
        assert completed_task.completed is True
        
        # Delete task
        deleted_task = task_service.delete_task(task.id)
        assert deleted_task.title == "Updated Task Title"
        
        # Verify task is deleted
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(task.id)
        
        assert len(task_service.tasks) == 0

    def test_ui_delete_workflow_simulation(self, task_service):
        """Simulate the UI delete workflow."""
        # Create multiple tasks like the UI would
        task1 = task_service.add_task("UI Task 1", "First task", "high")
        task2 = task_service.add_task("UI Task 2", "Second task", "medium")
        task3 = task_service.add_task("UI Task 3", "Third task", "low")
        
        initial_count = len(task_service.get_all_tasks())
        assert initial_count == 3
        
        # Simulate user clicking delete button on task2
        # This would set session state in real UI: st.session_state.task_to_delete = task2.id
        task_to_delete_id = task2.id
        
        # Simulate user confirming deletion
        # This would happen when user clicks "Yes, Delete" button
        try:
            deleted_task = task_service.delete_task(task_to_delete_id)
            assert deleted_task.id == task2.id
            assert deleted_task.title == "UI Task 2"
            
            # Verify task list is updated
            remaining_tasks = task_service.get_all_tasks()
            assert len(remaining_tasks) == 2
            
            # Verify the correct task was deleted
            remaining_titles = [task.title for task in remaining_tasks]
            assert "UI Task 1" in remaining_titles
            assert "UI Task 3" in remaining_titles
            assert "UI Task 2" not in remaining_titles
            
        except TaskNotFoundException:
            pytest.fail("Task should exist and be deletable")

    def test_search_and_delete_workflow(self, task_service):
        """Test the search and delete workflow from the search page."""
        # Create tasks with searchable content
        task1 = task_service.add_task("Project Alpha", "Work on alpha project", "high")
        task2 = task_service.add_task("Project Beta", "Work on beta project", "medium")
        task3 = task_service.add_task("Meeting Notes", "Take notes in meeting", "low")
        
        # Simulate search functionality
        search_results = task_service.search_tasks("project")
        assert len(search_results) == 2
        
        # Simulate user selecting a task from search results
        selected_task = search_results[0]  # Project Alpha
        
        # Simulate user clicking delete in task details view
        deleted_task = task_service.delete_task(selected_task.id)
        assert deleted_task.title == "Project Alpha"
        
        # Verify search results are updated
        updated_search_results = task_service.search_tasks("project")
        assert len(updated_search_results) == 1
        assert updated_search_results[0].title == "Project Beta"

    def test_delete_completed_task(self, task_service):
        """Test deleting a completed task."""
        # Create and complete a task
        task = task_service.add_task("Task to Complete and Delete", "Test task", "medium")
        completed_task = task_service.complete_task(task.id)
        assert completed_task.completed is True
        
        # Delete the completed task
        deleted_task = task_service.delete_task(task.id)
        assert deleted_task.completed is True
        assert deleted_task.title == "Task to Complete and Delete"
        
        # Verify task is gone
        assert len(task_service.tasks) == 0

    def test_delete_nonexistent_task_error_handling(self, task_service):
        """Test error handling when trying to delete a non-existent task."""
        # Try to delete a task that doesn't exist
        with pytest.raises(TaskNotFoundException) as exc_info:
            task_service.delete_task(999)
        
        assert "Task with ID 999 not found" in str(exc_info.value)

    def test_persistence_across_service_instances(self, temp_storage_file):
        """Test that delete operations persist across service instances."""
        # Create first service instance and add tasks
        service1 = TaskService(temp_storage_file)
        task1 = service1.add_task("Persistent Task 1")
        task2 = service1.add_task("Persistent Task 2")
        task3 = service1.add_task("Persistent Task 3")
        
        # Delete one task
        service1.delete_task(task2.id)
        
        # Create second service instance (simulates app restart)
        service2 = TaskService(temp_storage_file)
        
        # Verify the deletion persisted
        assert len(service2.tasks) == 2
        
        remaining_titles = [task.title for task in service2.tasks]
        assert "Persistent Task 1" in remaining_titles
        assert "Persistent Task 3" in remaining_titles
        assert "Persistent Task 2" not in remaining_titles
        
        # Verify the deleted task cannot be retrieved
        with pytest.raises(TaskNotFoundException):
            service2.get_task_by_id(task2.id)

    def test_filter_and_delete_workflow(self, task_service):
        """Test filtering tasks and then deleting from filtered results."""
        # Create tasks with different priorities and completion status
        task1 = task_service.add_task("High Priority Task", "Important", "high")
        task2 = task_service.add_task("Medium Priority Task", "Normal", "medium")
        task3 = task_service.add_task("Low Priority Task", "Not urgent", "low")
        
        # Complete one task
        task_service.complete_task(task2.id)
        
        # Simulate filtering by priority (high priority tasks)
        all_tasks = task_service.get_all_tasks()
        high_priority_tasks = [task for task in all_tasks if task.priority.lower() == "high"]
        assert len(high_priority_tasks) == 1
        
        # Delete the high priority task
        deleted_task = task_service.delete_task(high_priority_tasks[0].id)
        assert deleted_task.priority == "high"
        
        # Verify filtering still works after deletion
        remaining_tasks = task_service.get_all_tasks()
        high_priority_remaining = [task for task in remaining_tasks if task.priority.lower() == "high"]
        assert len(high_priority_remaining) == 0
        
        # Verify other tasks remain
        assert len(remaining_tasks) == 2