"""
Integration tests for the task management system.
"""

import unittest
import sys
import os
import tempfile
import json
import shutil

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskManagementIntegration(unittest.TestCase):
    """Integration tests for the task management system."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.storage_file = os.path.join(self.test_dir, "tasks.json")
        
        # Initialize a fresh TaskService for each test
        self.task_service = TaskService(self.storage_file)

    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)

    def test_complete_workflow(self):
        """Test a complete task management workflow."""
        # 1. Add several tasks
        task1 = self.task_service.add_task("Task 1", "Description 1", "high")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        task3 = self.task_service.add_task("Task 3", "Description 3", "low")
        
        # Verify tasks were added correctly
        self.assertEqual(len(self.task_service.get_all_tasks()), 3)
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)
        
        # 2. Update a task
        updated_task = self.task_service.update_task(2, title="Updated Task 2", priority="high")
        self.assertEqual(updated_task.title, "Updated Task 2")
        self.assertEqual(updated_task.priority, "high")
        
        # 3. Complete a task
        completed_task = self.task_service.complete_task(1)
        self.assertTrue(completed_task.completed)
        
        # 4. Search for tasks
        search_results = self.task_service.search_tasks("Updated")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].id, 2)
        
        # 5. Delete a task
        deleted_task = self.task_service.delete_task(3)
        self.assertEqual(deleted_task.id, 3)
        
        # 6. Verify final state
        tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 2)
        
        # 7. Verify that the task file contains the correct data
        with open(self.storage_file, 'r') as f:
            saved_data = json.load(f)
            self.assertEqual(len(saved_data), 2)
            self.assertEqual(saved_data[0]["id"], 1)
            self.assertTrue(saved_data[0]["completed"])
            self.assertEqual(saved_data[1]["id"], 2)
            self.assertEqual(saved_data[1]["title"], "Updated Task 2")

    def test_error_handling(self):
        """Test error handling for various operations."""
        # 1. Try to get a non-existent task
        with self.assertRaises(TaskNotFoundException):
            self.task_service.get_task_by_id(999)
        
        # 2. Add a task and then try to retrieve it
        task = self.task_service.add_task("Test Task")
        retrieved_task = self.task_service.get_task_by_id(1)
        self.assertEqual(retrieved_task.id, 1)
        
        # 3. Try to update a non-existent task
        with self.assertRaises(TaskNotFoundException):
            self.task_service.update_task(999, title="Updated Title")
        
        # 4. Try to complete a non-existent task
        with self.assertRaises(TaskNotFoundException):
            self.task_service.complete_task(999)
        
        # 5. Try to delete a non-existent task
        with self.assertRaises(TaskNotFoundException):
            self.task_service.delete_task(999)


if __name__ == "__main__":
    unittest.main()