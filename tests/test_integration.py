"""
Integration tests for the task manager application.
"""

import pytest
import tempfile
import os
import json
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskManagerIntegration:
    """Integration tests for the complete task manager workflow."""

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

    def test_complete_task_workflow(self):
        """Test the complete workflow of task management."""
        # 1. Add tasks
        task1 = self.service.add_task("Buy groceries", "Milk, bread, eggs", "high")
        task2 = self.service.add_task("Call dentist", "Schedule appointment", "medium")
        task3 = self.service.add_task("Read book", "Finish chapter 5", "low")
        
        # Verify tasks were added
        assert len(self.service.tasks) == 3
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        
        # 2. List all tasks (should show all active tasks)
        active_tasks = self.service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 3
        
        # 3. Complete a task
        completed_task = self.service.complete_task(task1.id)
        assert completed_task.completed is True
        
        # 4. List active tasks (should show 2 now)
        active_tasks = self.service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 2
        
        # 5. List all tasks including completed
        all_tasks = self.service.get_all_tasks(show_completed=True)
        assert len(all_tasks) == 3
        
        # 6. Search for tasks
        search_results = self.service.search_tasks("call")
        assert len(search_results) == 1
        assert search_results[0].title == "Call dentist"
        
        # 7. Update a task
        updated_task = self.service.update_task(
            task2.id,
            title="Call dentist - URGENT",
            priority="high"
        )
        assert updated_task.title == "Call dentist - URGENT"
        assert updated_task.priority == "high"
        
        # 8. Delete a task
        deleted_task = self.service.delete_task(task3.id)
        assert deleted_task.id == task3.id
        assert len(self.service.tasks) == 2
        
        # 9. Verify task is gone
        with pytest.raises(TaskNotFoundException):
            self.service.get_task_by_id(task3.id)

    def test_persistence_across_service_instances(self):
        """Test that data persists across different service instances."""
        # Add tasks with first service instance
        task1 = self.service.add_task("Persistent Task 1", "Description 1", "high")
        task2 = self.service.add_task("Persistent Task 2", "Description 2", "low")
        
        # Complete one task
        self.service.complete_task(task1.id)
        
        # Create new service instance
        new_service = TaskService(storage_file=self.temp_file.name)
        
        # Verify data was loaded correctly
        assert len(new_service.tasks) == 2
        
        loaded_task1 = new_service.get_task_by_id(task1.id)
        loaded_task2 = new_service.get_task_by_id(task2.id)
        
        assert loaded_task1.completed is True
        assert loaded_task2.completed is False
        assert loaded_task1.title == "Persistent Task 1"
        assert loaded_task2.title == "Persistent Task 2"
        
        # Add another task with new service
        task3 = new_service.add_task("New Task")
        assert task3.id == 3  # Should continue ID sequence
        
        # Verify with third service instance
        third_service = TaskService(storage_file=self.temp_file.name)
        assert len(third_service.tasks) == 3

    def test_search_functionality_comprehensive(self):
        """Test comprehensive search functionality."""
        # Add diverse tasks
        self.service.add_task("Meeting with client", "Discuss project requirements", "high")
        self.service.add_task("Code review", "Review pull request #123", "medium")
        self.service.add_task("Team meeting", "Weekly standup meeting", "low")
        self.service.add_task("Buy coffee", "Get coffee for the office", "low")
        self.service.add_task("Project planning", "Plan next sprint", "high")
        
        # Test search by title
        meeting_tasks = self.service.search_tasks("meeting")
        assert len(meeting_tasks) == 2
        
        # Test search by description
        project_tasks = self.service.search_tasks("project")
        assert len(project_tasks) == 2
        
        # Test case insensitive search
        code_tasks = self.service.search_tasks("CODE")
        assert len(code_tasks) == 1
        
        # Test partial word search
        buy_tasks = self.service.search_tasks("buy")
        assert len(buy_tasks) == 1
        
        # Test no results
        no_results = self.service.search_tasks("nonexistent")
        assert len(no_results) == 0

    def test_priority_and_completion_workflow(self):
        """Test workflow involving different priorities and completion states."""
        # Add tasks with different priorities
        high_task = self.service.add_task("Critical Bug Fix", "Fix production issue", "high")
        medium_task = self.service.add_task("Feature Development", "Implement new feature", "medium")
        low_task = self.service.add_task("Documentation", "Update README", "low")
        
        # Complete tasks in different order
        self.service.complete_task(low_task.id)
        self.service.complete_task(high_task.id)
        
        # Get active tasks
        active_tasks = self.service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 1
        assert active_tasks[0].priority == "medium"
        
        # Get all tasks
        all_tasks = self.service.get_all_tasks(show_completed=True)
        completed_tasks = [task for task in all_tasks if task.completed]
        active_tasks = [task for task in all_tasks if not task.completed]
        
        assert len(completed_tasks) == 2
        assert len(active_tasks) == 1
        
        # Verify priorities are preserved
        priorities = [task.priority for task in all_tasks]
        assert "high" in priorities
        assert "medium" in priorities
        assert "low" in priorities

    def test_task_update_comprehensive(self):
        """Test comprehensive task update functionality."""
        # Add a task
        task = self.service.add_task("Original Task", "Original description", "low")
        
        # Update title only
        self.service.update_task(task.id, title="Updated Title")
        updated_task = self.service.get_task_by_id(task.id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original description"
        assert updated_task.priority == "low"
        
        # Update description only
        self.service.update_task(task.id, description="Updated description")
        updated_task = self.service.get_task_by_id(task.id)
        assert updated_task.description == "Updated description"
        assert updated_task.title == "Updated Title"
        
        # Update priority only
        self.service.update_task(task.id, priority="high")
        updated_task = self.service.get_task_by_id(task.id)
        assert updated_task.priority == "high"
        
        # Update completion status
        self.service.update_task(task.id, completed=True)
        updated_task = self.service.get_task_by_id(task.id)
        assert updated_task.completed is True
        
        # Update multiple fields at once
        self.service.update_task(
            task.id,
            title="Final Title",
            description="Final description",
            priority="medium",
            completed=False
        )
        final_task = self.service.get_task_by_id(task.id)
        assert final_task.title == "Final Title"
        assert final_task.description == "Final description"
        assert final_task.priority == "medium"
        assert final_task.completed is False

    def test_edge_cases_and_error_handling(self):
        """Test edge cases and error handling."""
        # Test with empty task list
        assert len(self.service.get_all_tasks()) == 0
        assert len(self.service.search_tasks("anything")) == 0
        
        # Test operations on non-existent tasks
        with pytest.raises(TaskNotFoundException):
            self.service.get_task_by_id(999)
        
        with pytest.raises(TaskNotFoundException):
            self.service.update_task(999, title="New Title")
        
        with pytest.raises(TaskNotFoundException):
            self.service.complete_task(999)
        
        with pytest.raises(TaskNotFoundException):
            self.service.delete_task(999)
        
        # Add a task and test valid operations
        task = self.service.add_task("Test Task")
        
        # Test valid operations
        assert self.service.get_task_by_id(task.id) is not None
        self.service.update_task(task.id, title="Updated")
        self.service.complete_task(task.id)
        
        # Test that completed task is still accessible
        completed_task = self.service.get_task_by_id(task.id)
        assert completed_task.completed is True
        
        # Delete the task
        self.service.delete_task(task.id)
        
        # Verify it's gone
        with pytest.raises(TaskNotFoundException):
            self.service.get_task_by_id(task.id)

    def test_file_operations_and_data_integrity(self):
        """Test file operations and data integrity."""
        # Add tasks
        task1 = self.service.add_task("Task 1", "Description 1", "high")
        task2 = self.service.add_task("Task 2", "Description 2", "medium")
        
        # Verify file was created and contains correct data
        assert os.path.exists(self.temp_file.name)
        
        with open(self.temp_file.name, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 2
        assert data[0]['id'] == task1.id
        assert data[0]['title'] == "Task 1"
        assert data[1]['id'] == task2.id
        assert data[1]['title'] == "Task 2"
        
        # Modify a task and verify file is updated
        self.service.update_task(task1.id, title="Modified Task 1")
        
        with open(self.temp_file.name, 'r') as f:
            updated_data = json.load(f)
        
        assert updated_data[0]['title'] == "Modified Task 1"
        
        # Delete a task and verify file is updated
        self.service.delete_task(task2.id)
        
        with open(self.temp_file.name, 'r') as f:
            final_data = json.load(f)
        
        assert len(final_data) == 1
        assert final_data[0]['id'] == task1.id