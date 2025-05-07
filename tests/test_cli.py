"""
Tests for the CLI functionality.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cli import main
from src.services.task_service import TaskService
from src.models.task import Task

class TestCliApplication(unittest.TestCase):
    """Test cases for the CLI application."""

    def setUp(self):
        """Set up test fixtures."""
        self.task_service_patcher = patch('src.cli.TaskService')
        self.mock_task_service_class = self.task_service_patcher.start()
        self.mock_task_service = MagicMock(spec=TaskService)
        self.mock_task_service_class.return_value = self.mock_task_service
        
        # Create some sample tasks for testing
        self.sample_tasks = [
            Task(1, "Task 1", "Description 1", "high", False),
            Task(2, "Task 2", "Description 2", "medium", True),
            Task(3, "Task 3", "Description 3", "low", False)
        ]
        
        # Setup standard input/output patching
        self.stdin_patcher = patch('sys.stdin', StringIO())
        self.stdout_patcher = patch('sys.stdout', StringIO())
        self.mock_stdin = self.stdin_patcher.start()
        self.mock_stdout = self.stdout_patcher.start()

    def tearDown(self):
        """Tear down test fixtures."""
        self.task_service_patcher.stop()
        self.stdin_patcher.stop()
        self.stdout_patcher.stop()

    @patch('builtins.input')
    @patch('src.cli.argparse.ArgumentParser.parse_args')
    def test_add_task_command(self, mock_parse_args, mock_input):
        """Test the add task command."""
        # Setup mock arguments
        mock_args = MagicMock()
        mock_args.command = "add"
        mock_parse_args.return_value = mock_args
        
        # Setup mock input responses
        mock_input.side_effect = ["Test Task", "Test Description", "high"]
        
        # Setup mock task service
        new_task = Task(1, "Test Task", "Test Description", "high")
        self.mock_task_service.add_task.return_value = new_task
        
        # Call the main function
        with patch('sys.argv', ['cli.py', 'add']):
            main()
            
        # Assert that add_task was called with the correct arguments
        self.mock_task_service.add_task.assert_called_once_with(
            "Test Task", "Test Description", "high"
        )

    @patch('src.cli.argparse.ArgumentParser.parse_args')
    def test_list_tasks_command(self, mock_parse_args):
        """Test the list tasks command."""
        # Setup mock arguments
        mock_args = MagicMock()
        mock_args.command = "list"
        mock_args.all = False
        mock_parse_args.return_value = mock_args
        
        # Setup mock task service
        self.mock_task_service.get_all_tasks.return_value = self.sample_tasks
        
        # Call the main function
        with patch('sys.argv', ['cli.py', 'list']):
            main()
            
        # Assert that get_all_tasks was called with the correct arguments
        self.mock_task_service.get_all_tasks.assert_called_once_with(show_completed=False)

    @patch('src.cli.argparse.ArgumentParser.parse_args')
    def test_complete_task_command(self, mock_parse_args):
        """Test the complete task command."""
        # Setup mock arguments
        mock_args = MagicMock()
        mock_args.command = "complete"
        mock_args.id = 1
        mock_parse_args.return_value = mock_args
        
        # Setup mock task service
        completed_task = Task(1, "Task 1", "Description 1", "high", True)
        self.mock_task_service.complete_task.return_value = completed_task
        
        # Call the main function
        with patch('sys.argv', ['cli.py', 'complete', '1']):
            main()
            
        # Assert that complete_task was called with the correct arguments
        self.mock_task_service.complete_task.assert_called_once_with(1)

    @patch('src.cli.argparse.ArgumentParser.parse_args')
    def test_delete_task_command(self, mock_parse_args):
        """Test the delete task command."""
        # Setup mock arguments
        mock_args = MagicMock()
        mock_args.command = "delete"
        mock_args.id = 1
        mock_parse_args.return_value = mock_args
        
        # Setup mock task service
        deleted_task = Task(1, "Task 1", "Description 1", "high")
        self.mock_task_service.delete_task.return_value = deleted_task
        
        # Call the main function
        with patch('sys.argv', ['cli.py', 'delete', '1']):
            main()
            
        # Assert that delete_task was called with the correct arguments
        self.mock_task_service.delete_task.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()