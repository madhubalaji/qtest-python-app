"""
Tests for the CLI module.
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the project root to the path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cli import main
from src.utils.exceptions import TaskNotFoundException


class TestCLI:
    """Test cases for the CLI module."""

    @pytest.fixture
    def temp_config_dir(self):
        """Create a temporary config directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def mock_task_service(self):
        """Create a mock TaskService for testing."""
        mock_service = MagicMock()
        return mock_service

    def test_add_task_command(self, temp_config_dir, mock_task_service, capsys):
        """Test adding a task via CLI."""
        # Mock the task that would be returned
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task_service.add_task.return_value = mock_task

        test_args = ["add", "Test Task", "-d", "Test description", "-p", "high"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            mock_task_service.add_task.assert_called_once_with("Test Task", "Test description", "high")
            captured = capsys.readouterr()
            assert "Task 'Test Task' added successfully with ID 1" in captured.out

    def test_add_task_with_defaults(self, temp_config_dir, mock_task_service, capsys):
        """Test adding a task with default values."""
        mock_task = MagicMock()
        mock_task.id = 2
        mock_task.title = "Simple Task"
        mock_task_service.add_task.return_value = mock_task

        test_args = ["add", "Simple Task"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            mock_task_service.add_task.assert_called_once_with("Simple Task", "", "medium")
            captured = capsys.readouterr()
            assert "Task 'Simple Task' added successfully with ID 2" in captured.out

    def test_list_tasks_command(self, temp_config_dir, mock_task_service, capsys):
        """Test listing tasks via CLI."""
        # Create mock tasks
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task 1"
        mock_task1.priority = "high"
        mock_task1.completed = False
        mock_task1.created_at = "2023-01-01 12:00:00"
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Task 2"
        mock_task2.priority = "medium"
        mock_task2.completed = True
        mock_task2.created_at = "2023-01-02 12:00:00"
        
        mock_task_service.get_all_tasks.return_value = [mock_task1, mock_task2]

        test_args = ["list"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            mock_task_service.get_all_tasks.assert_called_once_with(show_completed=False)
            captured = capsys.readouterr()
            assert "Task 1" in captured.out
            assert "Task 2" in captured.out
            assert "Active" in captured.out
            assert "Completed" in captured.out

    def test_list_all_tasks_command(self, temp_config_dir, mock_task_service, capsys):
        """Test listing all tasks including completed ones."""
        mock_task_service.get_all_tasks.return_value = []

        test_args = ["list", "--all"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            mock_task_service.get_all_tasks.assert_called_once_with(show_completed=True)

    def test_list_no_tasks(self, temp_config_dir, mock_task_service, capsys):
        """Test listing when no tasks exist."""
        mock_task_service.get_all_tasks.return_value = []

        test_args = ["list"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            captured = capsys.readouterr()
            assert "No tasks found" in captured.out

    def test_complete_task_command(self, temp_config_dir, mock_task_service, capsys):
        """Test completing a task via CLI."""
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task_service.complete_task.return_value = mock_task

        test_args = ["complete", "1"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            mock_task_service.complete_task.assert_called_once_with(1)
            captured = capsys.readouterr()
            assert "Task 1 marked as complete" in captured.out

    def test_delete_task_command(self, temp_config_dir, mock_task_service, capsys):
        """Test deleting a task via CLI."""
        mock_task = MagicMock()
        mock_task.title = "Deleted Task"
        mock_task_service.delete_task.return_value = mock_task

        test_args = ["delete", "1"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            mock_task_service.delete_task.assert_called_once_with(1)
            captured = capsys.readouterr()
            assert "Task 'Deleted Task' deleted successfully" in captured.out

    def test_search_tasks_command(self, temp_config_dir, mock_task_service, capsys):
        """Test searching for tasks via CLI."""
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Found Task"
        mock_task.priority = "high"
        mock_task.completed = False
        
        mock_task_service.search_tasks.return_value = [mock_task]

        test_args = ["search", "Found"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            mock_task_service.search_tasks.assert_called_once_with("Found")
            captured = capsys.readouterr()
            assert "Found 1 tasks matching 'Found'" in captured.out
            assert "Found Task" in captured.out

    def test_search_no_results(self, temp_config_dir, mock_task_service, capsys):
        """Test searching with no results."""
        mock_task_service.search_tasks.return_value = []

        test_args = ["search", "NonExistent"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            captured = capsys.readouterr()
            assert "No tasks found matching 'NonExistent'" in captured.out

    def test_view_task_command(self, temp_config_dir, mock_task_service, capsys):
        """Test viewing a task via CLI."""
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "View Task"
        mock_task.description = "Task description"
        mock_task.priority = "medium"
        mock_task.completed = False
        mock_task.created_at = "2023-01-01 12:00:00"
        
        mock_task_service.get_task_by_id.return_value = mock_task

        test_args = ["view", "1"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            mock_task_service.get_task_by_id.assert_called_once_with(1)
            captured = capsys.readouterr()
            assert "Task ID: 1" in captured.out
            assert "Title: View Task" in captured.out
            assert "Description: Task description" in captured.out
            assert "Priority: medium" in captured.out
            assert "Status: Active" in captured.out

    def test_view_completed_task(self, temp_config_dir, mock_task_service, capsys):
        """Test viewing a completed task."""
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Completed Task"
        mock_task.description = "Task description"
        mock_task.priority = "high"
        mock_task.completed = True
        mock_task.created_at = "2023-01-01 12:00:00"
        
        mock_task_service.get_task_by_id.return_value = mock_task

        test_args = ["view", "1"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            captured = capsys.readouterr()
            assert "Status: Completed" in captured.out

    def test_task_not_found_exception(self, temp_config_dir, mock_task_service, capsys):
        """Test handling TaskNotFoundException."""
        mock_task_service.get_task_by_id.side_effect = TaskNotFoundException("Task with ID 999 not found")

        test_args = ["view", "999"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            captured = capsys.readouterr()
            assert "Error: Task with ID 999 not found" in captured.out

    def test_unexpected_exception(self, temp_config_dir, mock_task_service, capsys):
        """Test handling unexpected exceptions."""
        mock_task_service.get_task_by_id.side_effect = Exception("Unexpected error")

        test_args = ["view", "1"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            captured = capsys.readouterr()
            assert "An unexpected error occurred: Unexpected error" in captured.out

    def test_no_command_shows_help(self, temp_config_dir, mock_task_service, capsys):
        """Test that no command shows help."""
        test_args = []
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            main()
            
            captured = capsys.readouterr()
            assert "usage:" in captured.out or "Task Manager - A CLI task management app" in captured.out

    def test_invalid_command_shows_help(self, temp_config_dir, mock_task_service, capsys):
        """Test that invalid command shows help."""
        test_args = ["invalid"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service), \
             patch('os.makedirs'):
            
            # This should raise SystemExit due to argparse
            with pytest.raises(SystemExit):
                main()

    def test_config_directory_creation(self, temp_config_dir):
        """Test that config directory is created."""
        mock_task_service = MagicMock()
        test_args = ["list"]
        
        with patch('sys.argv', ['cli.py'] + test_args), \
             patch('src.cli.TaskService', return_value=mock_task_service) as mock_service_class, \
             patch('os.makedirs') as mock_makedirs:
            
            main()
            
            # Verify that makedirs was called
            mock_makedirs.assert_called_once()
            # Verify that TaskService was initialized with the correct path
            mock_service_class.assert_called_once()
            args, kwargs = mock_service_class.call_args
            assert args[0].endswith('tasks.json')