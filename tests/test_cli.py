"""
Tests for the CLI module.
"""

import unittest
import os
import tempfile
import sys
from io import StringIO
from unittest.mock import patch

from src.cli import main
from src.services.task_service import TaskService


class TestCLI(unittest.TestCase):
    """Test cases for the CLI module."""

    def setUp(self):
        """Set up a temporary file for task storage and redirect stdout."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Create a patch for the storage file path
        self.storage_patcher = patch('src.cli.storage_file', self.temp_file.name)
        self.storage_patcher.start()
        
        # Capture stdout
        self.stdout_patcher = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.stdout_patcher.start()

    def tearDown(self):
        """Clean up the temporary file and restore stdout."""
        os.unlink(self.temp_file.name)
        self.storage_patcher.stop()
        self.stdout_patcher.stop()

    def test_add_task(self):
        """Test adding a task via CLI."""
        with patch('sys.argv', ['cli.py', 'add', 'Test Task', '-d', 'Test Description', '-p', 'high']):
            main()
        
        output = self.mock_stdout.getvalue()
        self.assertIn("Task 'Test Task' added successfully", output)
        
        # Verify the task was added
        task_service = TaskService(self.temp_file.name)
        tasks = task_service.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test Task")
        self.assertEqual(tasks[0].description, "Test Description")
        self.assertEqual(tasks[0].priority, "high")

    def test_list_tasks(self):
        """Test listing tasks via CLI."""
        # Add some tasks first
        task_service = TaskService(self.temp_file.name)
        task_service.add_task("Task 1", "Description 1", "low")
        task_service.add_task("Task 2", "Description 2", "medium")
        task_service.add_task("Task 3", "Description 3", "high")
        task_service.complete_task(2)  # Mark Task 2 as complete
        
        # Test listing active tasks
        with patch('sys.argv', ['cli.py', 'list']):
            main()
        
        output = self.mock_stdout.getvalue()
        self.assertIn("Task 1", output)
        self.assertIn("Task 3", output)
        self.assertNotIn("Task 2", output)  # Task 2 is completed
        
        # Clear stdout
        self.mock_stdout.truncate(0)
        self.mock_stdout.seek(0)
        
        # Test listing all tasks including completed
        with patch('sys.argv', ['cli.py', 'list', '-a']):
            main()
        
        output = self.mock_stdout.getvalue()
        self.assertIn("Task 1", output)
        self.assertIn("Task 2", output)
        self.assertIn("Task 3", output)

    def test_complete_task(self):
        """Test completing a task via CLI."""
        # Add a task first
        task_service = TaskService(self.temp_file.name)
        task = task_service.add_task("Test Task")
        
        with patch('sys.argv', ['cli.py', 'complete', str(task.id)]):
            main()
        
        output = self.mock_stdout.getvalue()
        self.assertIn(f"Task {task.id} marked as complete", output)
        
        # Verify the task was marked as complete
        updated_task = task_service.get_task_by_id(task.id)
        self.assertTrue(updated_task.completed)

    def test_delete_task(self):
        """Test deleting a task via CLI."""
        # Add a task first
        task_service = TaskService(self.temp_file.name)
        task = task_service.add_task("Test Task")
        
        with patch('sys.argv', ['cli.py', 'delete', str(task.id)]):
            main()
        
        output = self.mock_stdout.getvalue()
        self.assertIn(f"Task 'Test Task' deleted successfully", output)
        
        # Verify the task was deleted
        tasks = task_service.get_all_tasks()
        self.assertEqual(len(tasks), 0)

    def test_search_tasks(self):
        """Test searching for tasks via CLI."""
        # Add some tasks first
        task_service = TaskService(self.temp_file.name)
        task_service.add_task("Buy groceries", "Get milk and eggs")
        task_service.add_task("Clean house", "Vacuum and dust")
        task_service.add_task("Buy milk", "Get whole milk")
        
        with patch('sys.argv', ['cli.py', 'search', 'milk']):
            main()
        
        output = self.mock_stdout.getvalue()
        self.assertIn("Found 2 tasks matching 'milk'", output)
        self.assertIn("Buy groceries", output)
        self.assertIn("Buy milk", output)
        self.assertNotIn("Clean house", output)

    def test_view_task(self):
        """Test viewing a task via CLI."""
        # Add a task first
        task_service = TaskService(self.temp_file.name)
        task = task_service.add_task("Test Task", "Test Description", "high")
        
        with patch('sys.argv', ['cli.py', 'view', str(task.id)]):
            main()
        
        output = self.mock_stdout.getvalue()
        self.assertIn("Task ID: 1", output)
        self.assertIn("Title: Test Task", output)
        self.assertIn("Description: Test Description", output)
        self.assertIn("Priority: high", output)
        self.assertIn("Status: Active", output)

    def test_task_not_found(self):
        """Test handling of task not found errors."""
        with patch('sys.argv', ['cli.py', 'view', '999']):
            main()
        
        output = self.mock_stdout.getvalue()
        self.assertIn("Error: Task with ID 999 not found", output)

    def test_no_command(self):
        """Test CLI with no command."""
        with patch('sys.argv', ['cli.py']):
            main()
        
        output = self.mock_stdout.getvalue()
        self.assertIn("usage:", output)  # Should show help


if __name__ == "__main__":
    unittest.main()