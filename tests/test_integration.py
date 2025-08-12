"""
Integration tests for the task manager application.
"""

import pytest
import os
import tempfile
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskManagerIntegration:
    """Integration tests for the complete task management workflow."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.task_service = TaskService(self.temp_file.name)

    def teardown_method(self):
        """Clean up after each test method."""
        # Remove the temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_complete_task_workflow(self):
        """Test the complete task management workflow."""
        # Add a task
        task = self.task_service.add_task(
            title="Complete Workflow Task",
            description="Test the complete workflow",
            priority="high"
        )
        
        assert task.id == 1
        assert task.completed is False
        
        # Update the task
        updated_task = self.task_service.update_task(
            task.id,
            description="Updated description"
        )
        assert updated_task.description == "Updated description"
        
        # Complete the task
        completed_task = self.task_service.complete_task(task.id)
        assert completed_task.completed is True
        
        # Verify task is in completed state
        retrieved_task = self.task_service.get_task_by_id(task.id)
        assert retrieved_task.completed is True

    def test_multiple_tasks_management(self):
        """Test managing multiple tasks."""
        # Add multiple tasks
        task1 = self.task_service.add_task("Task 1", priority="low")
        task2 = self.task_service.add_task("Task 2", priority="medium")
        task3 = self.task_service.add_task("Task 3", priority="high")
        
        # Verify all tasks are added
        all_tasks = self.task_service.get_all_tasks()
        assert len(all_tasks) == 3
        
        # Complete one task
        self.task_service.complete_task(task2.id)
        
        # Get active tasks only
        active_tasks = self.task_service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 2
        
        # Delete one task
        self.task_service.delete_task(task1.id)
        
        # Verify task count
        remaining_tasks = self.task_service.get_all_tasks()
        assert len(remaining_tasks) == 2

    def test_search_and_filter_workflow(self):
        """Test search and filtering functionality."""
        # Add tasks with different content
        task1 = self.task_service.add_task("Python Development", "Learn Python programming")
        task2 = self.task_service.add_task("Java Programming", "Build Java application")
        task3 = self.task_service.add_task("Database Design", "Design Python database")
        
        # Search for Python-related tasks
        python_tasks = self.task_service.search_tasks("Python")
        assert len(python_tasks) == 2
        
        # Complete one Python task
        self.task_service.complete_task(task1.id)
        
        # Search should still return both (including completed)
        python_tasks_after_completion = self.task_service.search_tasks("Python")
        assert len(python_tasks_after_completion) == 2
        
        # Filter active tasks
        active_tasks = self.task_service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 2

    def test_persistence_across_sessions(self):
        """Test that data persists across different service instances."""
        # Add tasks in first session
        task1 = self.task_service.add_task("Persistent Task 1")
        task2 = self.task_service.add_task("Persistent Task 2")
        self.task_service.complete_task(task1.id)
        
        # Create new service instance (simulating app restart)
        new_service = TaskService(self.temp_file.name)
        
        # Verify data persistence
        loaded_tasks = new_service.get_all_tasks()
        assert len(loaded_tasks) == 2
        
        # Verify task states
        loaded_task1 = new_service.get_task_by_id(task1.id)
        loaded_task2 = new_service.get_task_by_id(task2.id)
        
        assert loaded_task1.completed is True
        assert loaded_task2.completed is False

    def test_error_handling_workflow(self):
        """Test error handling in various scenarios."""
        # Add a task
        task = self.task_service.add_task("Test Task")
        
        # Try to get non-existent task
        with pytest.raises(TaskNotFoundException):
            self.task_service.get_task_by_id(999)
        
        # Try to update non-existent task
        with pytest.raises(TaskNotFoundException):
            self.task_service.update_task(999, title="Non-existent")
        
        # Try to complete non-existent task
        with pytest.raises(TaskNotFoundException):
            self.task_service.complete_task(999)
        
        # Try to delete non-existent task
        with pytest.raises(TaskNotFoundException):
            self.task_service.delete_task(999)
        
        # Verify original task is still intact
        retrieved_task = self.task_service.get_task_by_id(task.id)
        assert retrieved_task.title == "Test Task"

    def test_task_lifecycle(self):
        """Test complete task lifecycle from creation to deletion."""
        # Create task
        task = self.task_service.add_task(
            title="Lifecycle Task",
            description="Test complete lifecycle",
            priority="medium"
        )
        
        # Verify initial state
        assert task.completed is False
        assert task.priority == "medium"
        
        # Update task
        self.task_service.update_task(
            task.id,
            description="Updated lifecycle description",
            priority="high"
        )
        
        # Verify update
        updated_task = self.task_service.get_task_by_id(task.id)
        assert updated_task.description == "Updated lifecycle description"
        assert updated_task.priority == "high"
        
        # Complete task
        self.task_service.complete_task(task.id)
        completed_task = self.task_service.get_task_by_id(task.id)
        assert completed_task.completed is True
        
        # Delete task
        deleted_task = self.task_service.delete_task(task.id)
        assert deleted_task.id == task.id
        
        # Verify deletion
        with pytest.raises(TaskNotFoundException):
            self.task_service.get_task_by_id(task.id)

    def test_bulk_operations(self):
        """Test bulk operations on multiple tasks."""
        # Add multiple tasks
        tasks = []
        for i in range(5):
            task = self.task_service.add_task(f"Bulk Task {i+1}")
            tasks.append(task)
        
        # Complete some tasks
        for i in [0, 2, 4]:  # Complete tasks 1, 3, 5
            self.task_service.complete_task(tasks[i].id)
        
        # Verify completion status
        all_tasks = self.task_service.get_all_tasks()
        completed_count = sum(1 for task in all_tasks if task.completed)
        assert completed_count == 3
        
        # Delete completed tasks
        for task in all_tasks:
            if task.completed:
                self.task_service.delete_task(task.id)
        
        # Verify remaining tasks
        remaining_tasks = self.task_service.get_all_tasks()
        assert len(remaining_tasks) == 2
        assert all(not task.completed for task in remaining_tasks)