"""
Tests for the CLI module.
"""

import unittest
import sys
import io
import os
from unittest.mock import patch, MagicMock
from src.cli import main
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestCLI(unittest.TestCase):
    """Test cases for the CLI module."""

    @patch("src.cli.TaskService")
    def test_add_command(self, mock_task_service_class):
        """Test the 'add' command."""
        # Setup mock
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service
        
        # Create a mock task to be returned
        mock_task = Task(1, "Test Task", "Test Description", "high")
        mock_task_service.add_task.return_value = mock_task
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Run the command
        with patch.object(sys, 'argv', ['cli.py', 'add', 'Test Task', '-d', 'Test Description', '-p', 'high']):
            main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify the task service was called correctly
        mock_task_service.add_task.assert_called_once_with('Test Task', 'Test Description', 'high')
        
        # Check the output
        self.assertIn("Task 'Test Task' added successfully with ID 1", captured_output.getvalue())

    @patch("src.cli.TaskService")
    def test_list_command(self, mock_task_service_class):
        """Test the 'list' command."""
        # Setup mock
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service
        
        # Create mock tasks to be returned
        task1 = Task(1, "Task 1", priority="low")
        task2 = Task(2, "Task 2", priority="medium")
        mock_task_service.get_all_tasks.return_value = [task1, task2]
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Run the command
        with patch.object(sys, 'argv', ['cli.py', 'list']):
            main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify the task service was called correctly
        mock_task_service.get_all_tasks.assert_called_once_with(show_completed=False)
        
        # Check the output
        output = captured_output.getvalue()
        self.assertIn("Task 1", output)
        self.assertIn("Task 2", output)

    @patch("src.cli.TaskService")
    def test_list_all_command(self, mock_task_service_class):
        """Test the 'list -a' command."""
        # Setup mock
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service
        
        # Create mock tasks to be returned
        task1 = Task(1, "Task 1", completed=False)
        task2 = Task(2, "Task 2", completed=True)
        mock_task_service.get_all_tasks.return_value = [task1, task2]
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Run the command
        with patch.object(sys, 'argv', ['cli.py', 'list', '-a']):
            main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify the task service was called correctly
        mock_task_service.get_all_tasks.assert_called_once_with(show_completed=True)
        
        # Check the output
        output = captured_output.getvalue()
        self.assertIn("Task 1", output)
        self.assertIn("Task 2", output)

    @patch("src.cli.TaskService")
    def test_complete_command(self, mock_task_service_class):
        """Test the 'complete' command."""
        # Setup mock
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service
        
        # Create a mock task to be returned
        mock_task = Task(1, "Test Task", completed=True)
        mock_task_service.complete_task.return_value = mock_task
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Run the command
        with patch.object(sys, 'argv', ['cli.py', 'complete', '1']):
            main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify the task service was called correctly
        mock_task_service.complete_task.assert_called_once_with(1)
        
        # Check the output
        self.assertIn("Task 1 marked as complete", captured_output.getvalue())

    @patch("src.cli.TaskService")
    def test_delete_command(self, mock_task_service_class):
        """Test the 'delete' command."""
        # Setup mock
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service
        
        # Create a mock task to be returned
        mock_task = Task(1, "Test Task")
        mock_task_service.delete_task.return_value = mock_task
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Run the command
        with patch.object(sys, 'argv', ['cli.py', 'delete', '1']):
            main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify the task service was called correctly
        mock_task_service.delete_task.assert_called_once_with(1)
        
        # Check the output
        self.assertIn("Task 'Test Task' deleted successfully", captured_output.getvalue())

    @patch("src.cli.TaskService")
    def test_search_command(self, mock_task_service_class):
        """Test the 'search' command."""
        # Setup mock
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service
        
        # Create mock tasks to be returned
        task1 = Task(1, "Apple Task")
        task2 = Task(2, "Apple Pie")
        mock_task_service.search_tasks.return_value = [task1, task2]
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Run the command
        with patch.object(sys, 'argv', ['cli.py', 'search', 'apple']):
            main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify the task service was called correctly
        mock_task_service.search_tasks.assert_called_once_with('apple')
        
        # Check the output
        output = captured_output.getvalue()
        self.assertIn("Found 2 tasks matching 'apple'", output)
        self.assertIn("Apple Task", output)
        self.assertIn("Apple Pie", output)

    @patch("src.cli.TaskService")
    def test_view_command(self, mock_task_service_class):
        """Test the 'view' command."""
        # Setup mock
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service
        
        # Create a mock task to be returned
        mock_task = Task(
            1, 
            "Test Task", 
            "Test Description", 
            "high", 
            False, 
            "2023-01-01 12:00:00"
        )
        mock_task_service.get_task_by_id.return_value = mock_task
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Run the command
        with patch.object(sys, 'argv', ['cli.py', 'view', '1']):
            main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify the task service was called correctly
        mock_task_service.get_task_by_id.assert_called_once_with(1)
        
        # Check the output
        output = captured_output.getvalue()
        self.assertIn("Task ID: 1", output)
        self.assertIn("Title: Test Task", output)
        self.assertIn("Description: Test Description", output)
        self.assertIn("Priority: high", output)
        self.assertIn("Status: Active", output)
        self.assertIn("Created at: 2023-01-01 12:00:00", output)

    @patch("src.cli.TaskService")
    def test_task_not_found_exception(self, mock_task_service_class):
        """Test handling of TaskNotFoundException."""
        # Setup mock
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service
        
        # Make the get_task_by_id method raise an exception
        mock_task_service.get_task_by_id.side_effect = TaskNotFoundException("Task with ID 999 not found")
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Run the command
        with patch.object(sys, 'argv', ['cli.py', 'view', '999']):
            main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify the task service was called correctly
        mock_task_service.get_task_by_id.assert_called_once_with(999)
        
        # Check the output
        self.assertIn("Error: Task with ID 999 not found", captured_output.getvalue())

    @patch("src.cli.TaskService")
    def test_no_command(self, mock_task_service_class):
        """Test running the CLI with no command."""
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Run with no command
        with patch.object(sys, 'argv', ['cli.py']):
            main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check that help text was printed
        self.assertIn("usage:", captured_output.getvalue().lower())


if __name__ == "__main__":
    unittest.main()