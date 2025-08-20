"""
Integration tests for the Streamlit app functionality.
"""

import os
import tempfile
import unittest
from unittest.mock import Mock, patch

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


class TestAppIntegration(unittest.TestCase):
    """Integration test cases for app functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.task_service = TaskService(self.temp_file.name)

    def tearDown(self):
        """Clean up after each test method."""
        # Remove the temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_delete_task_workflow(self):
        """Test the complete delete task workflow."""
        # Add some tasks
        task1 = self.task_service.add_task("Task to Keep", "Keep this task", "low")
        task2 = self.task_service.add_task("Task to Delete", "Delete this task", "high")
        task3 = self.task_service.add_task("Another Task", "Another task", "medium")
        
        initial_count = len(self.task_service.get_all_tasks())
        self.assertEqual(initial_count, 3)
        
        # Simulate the delete workflow
        # 1. User clicks delete button (sets task_to_delete in session state)
        task_to_delete_id = task2.id
        
        # 2. App retrieves task for confirmation
        task_to_delete = self.task_service.get_task_by_id(task_to_delete_id)
        self.assertEqual(task_to_delete.title, "Task to Delete")
        
        # 3. User confirms deletion
        deleted_task = self.task_service.delete_task(task_to_delete_id)
        
        # 4. Verify deletion was successful
        self.assertEqual(deleted_task.id, task_to_delete_id)
        self.assertEqual(deleted_task.title, "Task to Delete")
        
        # 5. Verify remaining tasks
        remaining_tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(remaining_tasks), 2)
        
        remaining_titles = [task.title for task in remaining_tasks]
        self.assertIn("Task to Keep", remaining_titles)
        self.assertIn("Another Task", remaining_titles)
        self.assertNotIn("Task to Delete", remaining_titles)

    def test_delete_nonexistent_task_error_handling(self):
        """Test error handling when trying to delete a non-existent task."""
        # Add a task
        task = self.task_service.add_task("Test Task", "Test Description", "medium")
        
        # Delete the task
        self.task_service.delete_task(task.id)
        
        # Try to delete the same task again (should raise exception)
        with self.assertRaises(TaskNotFoundException):
            self.task_service.delete_task(task.id)

    def test_delete_task_with_filtering(self):
        """Test delete functionality with task filtering scenarios."""
        # Add tasks with different priorities and completion status
        task1 = self.task_service.add_task("Low Priority", "Low priority task", "low")
        task2 = self.task_service.add_task("High Priority", "High priority task", "high")
        task3 = self.task_service.add_task("Medium Priority", "Medium priority task", "medium")
        
        # Complete one task
        self.task_service.complete_task(task2.id)
        
        # Test filtering scenarios before deletion
        all_tasks = self.task_service.get_all_tasks(show_completed=True)
        self.assertEqual(len(all_tasks), 3)
        
        active_tasks = self.task_service.get_all_tasks(show_completed=False)
        self.assertEqual(len(active_tasks), 2)
        
        # Delete a completed task
        deleted_task = self.task_service.delete_task(task2.id)
        self.assertTrue(deleted_task.completed)
        
        # Verify filtering still works after deletion
        all_tasks_after = self.task_service.get_all_tasks(show_completed=True)
        self.assertEqual(len(all_tasks_after), 2)
        
        active_tasks_after = self.task_service.get_all_tasks(show_completed=False)
        self.assertEqual(len(active_tasks_after), 2)

    def test_delete_task_search_functionality(self):
        """Test delete functionality in search context."""
        # Add tasks with searchable content
        task1 = self.task_service.add_task("Important Meeting", "Meeting with client", "high")
        task2 = self.task_service.add_task("Buy Groceries", "Buy milk and bread", "low")
        task3 = self.task_service.add_task("Important Report", "Write quarterly report", "medium")
        
        # Search for tasks containing "Important"
        search_results = self.task_service.search_tasks("Important")
        self.assertEqual(len(search_results), 2)
        
        # Delete one of the search results
        task_to_delete = search_results[0]  # "Important Meeting"
        deleted_task = self.task_service.delete_task(task_to_delete.id)
        
        # Verify deletion
        self.assertEqual(deleted_task.title, task_to_delete.title)
        
        # Search again to verify the deleted task is no longer found
        new_search_results = self.task_service.search_tasks("Important")
        self.assertEqual(len(new_search_results), 1)
        self.assertEqual(new_search_results[0].title, "Important Report")

    def test_delete_all_tasks_scenario(self):
        """Test deleting all tasks one by one."""
        # Add multiple tasks
        tasks = []
        for i in range(5):
            task = self.task_service.add_task(f"Task {i+1}", f"Description {i+1}", "medium")
            tasks.append(task)
        
        self.assertEqual(len(self.task_service.get_all_tasks()), 5)
        
        # Delete all tasks one by one
        for task in tasks:
            deleted_task = self.task_service.delete_task(task.id)
            self.assertEqual(deleted_task.id, task.id)
        
        # Verify no tasks remain
        self.assertEqual(len(self.task_service.get_all_tasks()), 0)
        
        # Verify search returns empty results
        search_results = self.task_service.search_tasks("Task")
        self.assertEqual(len(search_results), 0)

    def test_delete_task_id_reuse_prevention(self):
        """Test that deleted task IDs are not reused."""
        # Add a task
        task1 = self.task_service.add_task("First Task", "Description", "low")
        first_id = task1.id
        
        # Delete the task
        self.task_service.delete_task(first_id)
        
        # Add a new task
        task2 = self.task_service.add_task("Second Task", "Description", "medium")
        second_id = task2.id
        
        # Verify the new task has a different ID
        self.assertNotEqual(first_id, second_id)
        self.assertGreater(second_id, first_id)


if __name__ == '__main__':
    unittest.main()