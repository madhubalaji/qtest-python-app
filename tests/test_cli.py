"""
Unit tests for the CLI module.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO
from src.cli import main
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestCLI:
    """Test cases for the CLI module."""

    @pytest.fixture
    def mock_task_service(self):
        """Create a mock TaskService for testing."""
        mock_service = MagicMock()
        return mock_service

    @pytest.fixture
    def sample_task(self):
        """Create a sample task for testing."""
        return Task(
            task_id=1,
            title="Test Task",
            description="Test Description",
            priority="high",
            completed=False,
            created_at="2023-01-01 12:00:00"
        )

    def test_add_command_basic(self, mock_task_service, sample_task):
        """Test basic add command."""
        mock_task_service.add_task.return_value = sample_task
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'add', 'Test Task']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_task_service.add_task.assert_called_once_with('Test Task', '', 'medium')
                    mock_print.assert_called_with("Task 'Test Task' added successfully with ID 1.")

    def test_add_command_with_description_and_priority(self, mock_task_service, sample_task):
        """Test add command with description and priority."""
        mock_task_service.add_task.return_value = sample_task
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'add', 'Test Task', '-d', 'Test Description', '-p', 'high']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_task_service.add_task.assert_called_once_with('Test Task', 'Test Description', 'high')

    def test_list_command_with_tasks(self, mock_task_service, sample_task):
        """Test list command with existing tasks."""
        mock_task_service.get_all_tasks.return_value = [sample_task]
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'list']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_task_service.get_all_tasks.assert_called_once_with(show_completed=False)
                    # Check that task information is printed
                    print_calls = [call.args[0] for call in mock_print.call_args_list]
                    assert any("Test Task" in str(call) for call in print_calls)

    def test_list_command_with_all_flag(self, mock_task_service, sample_task):
        """Test list command with --all flag."""
        mock_task_service.get_all_tasks.return_value = [sample_task]
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'list', '--all']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_task_service.get_all_tasks.assert_called_once_with(show_completed=True)

    def test_list_command_no_tasks(self, mock_task_service):
        """Test list command with no tasks."""
        mock_task_service.get_all_tasks.return_value = []
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'list']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_print.assert_called_with("No tasks found.")

    def test_complete_command(self, mock_task_service, sample_task):
        """Test complete command."""
        completed_task = Task(1, "Test Task", completed=True)
        mock_task_service.complete_task.return_value = completed_task
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'complete', '1']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_task_service.complete_task.assert_called_once_with(1)
                    mock_print.assert_called_with("Task 1 marked as complete.")

    def test_delete_command(self, mock_task_service, sample_task):
        """Test delete command."""
        mock_task_service.delete_task.return_value = sample_task
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'delete', '1']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_task_service.delete_task.assert_called_once_with(1)
                    mock_print.assert_called_with("Task 'Test Task' deleted successfully.")

    def test_search_command_with_results(self, mock_task_service, sample_task):
        """Test search command with results."""
        mock_task_service.search_tasks.return_value = [sample_task]
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'search', 'test']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_task_service.search_tasks.assert_called_once_with('test')
                    print_calls = [call.args[0] for call in mock_print.call_args_list]
                    assert any("Found 1 tasks matching 'test'" in str(call) for call in print_calls)

    def test_search_command_no_results(self, mock_task_service):
        """Test search command with no results."""
        mock_task_service.search_tasks.return_value = []
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'search', 'nonexistent']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_print.assert_called_with("No tasks found matching 'nonexistent'.")

    def test_view_command(self, mock_task_service, sample_task):
        """Test view command."""
        mock_task_service.get_task_by_id.return_value = sample_task
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'view', '1']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_task_service.get_task_by_id.assert_called_once_with(1)
                    print_calls = [call.args[0] for call in mock_print.call_args_list]
                    assert any("Task ID: 1" in str(call) for call in print_calls)
                    assert any("Title: Test Task" in str(call) for call in print_calls)

    def test_task_not_found_exception_handling(self, mock_task_service):
        """Test handling of TaskNotFoundException."""
        mock_task_service.get_task_by_id.side_effect = TaskNotFoundException("Task with ID 999 not found")
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'view', '999']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_print.assert_called_with("Error: Task with ID 999 not found")

    def test_general_exception_handling(self, mock_task_service):
        """Test handling of general exceptions."""
        mock_task_service.get_task_by_id.side_effect = Exception("Unexpected error")
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'view', '1']):
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_print.assert_called_with("An unexpected error occurred: Unexpected error")

    def test_no_command_shows_help(self, mock_task_service):
        """Test that no command shows help."""
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py']):
                with patch('argparse.ArgumentParser.print_help') as mock_help:
                    main()
                    mock_help.assert_called_once()

    def test_invalid_command_shows_help(self, mock_task_service):
        """Test that invalid command shows help."""
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'invalid']):
                with pytest.raises(SystemExit):  # argparse exits on invalid command
                    main()

    @pytest.mark.parametrize("priority", ["low", "medium", "high"])
    def test_add_command_priority_validation(self, mock_task_service, sample_task, priority):
        """Test add command with different priority values."""
        mock_task_service.add_task.return_value = sample_task
        
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('sys.argv', ['cli.py', 'add', 'Test Task', '-p', priority]):
                with patch('builtins.print'):
                    main()
                    
                    mock_task_service.add_task.assert_called_once_with('Test Task', '', priority)

    def test_config_directory_creation(self, mock_task_service):
        """Test that config directory is created."""
        with patch('src.cli.TaskService', return_value=mock_task_service):
            with patch('os.makedirs') as mock_makedirs:
                with patch('sys.argv', ['cli.py', 'list']):
                    with patch('builtins.print'):
                        main()
                        
                        # Check that makedirs was called with exist_ok=True
                        mock_makedirs.assert_called_once()
                        args, kwargs = mock_makedirs.call_args
                        assert kwargs.get('exist_ok') is True

    def test_storage_file_path_construction(self, mock_task_service):
        """Test that storage file path is constructed correctly."""
        with patch('src.cli.TaskService') as mock_service_class:
            mock_service_class.return_value = mock_task_service
            with patch('sys.argv', ['cli.py', 'list']):
                with patch('builtins.print'):
                    main()
                    
                    # Check that TaskService was initialized with correct path
                    mock_service_class.assert_called_once()
                    args = mock_service_class.call_args[0]
                    assert args[0].endswith('tasks.json')
                    assert 'config' in args[0]