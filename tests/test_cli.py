"""
Tests for the CLI interface.
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from src.cli import main
from src.services.task_service import TaskService


class TestCLI:
    """Test cases for the CLI interface."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()

    def teardown_method(self):
        """Clean up after each test method."""
        # Remove the temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    @patch('src.cli.TaskService')
    @patch('sys.argv', ['cli.py', 'add', 'Test Task'])
    def test_add_task_basic(self, mock_task_service_class):
        """Test adding a basic task via CLI."""
        # Mock the service instance
        mock_service = MagicMock()
        mock_task_service_class.return_value = mock_service
        
        # Mock the task that would be returned
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_service.add_task.return_value = mock_task
        
        with patch('builtins.print') as mock_print:
            try:
                main()
            except SystemExit:
                pass  # argparse calls sys.exit, which is expected
            
            # Verify service was called correctly
            mock_service.add_task.assert_called_once_with("Test Task", "", "medium")

    @patch('src.cli.TaskService')
    @patch('sys.argv', ['cli.py', 'add', 'Important Task', '-d', 'Task description', '-p', 'high'])
    def test_add_task_with_options(self, mock_task_service_class):
        """Test adding a task with description and priority via CLI."""
        mock_service = MagicMock()
        mock_task_service_class.return_value = mock_service
        
        mock_task = MagicMock()
        mock_task.id = 1
        mock_service.add_task.return_value = mock_task
        
        with patch('builtins.print'):
            try:
                main()
            except SystemExit:
                pass
            
            mock_service.add_task.assert_called_once_with("Important Task", "Task description", "high")

    @patch('src.cli.TaskService')
    @patch('sys.argv', ['cli.py', 'list'])
    def test_list_tasks(self, mock_task_service_class):
        """Test listing tasks via CLI."""
        mock_service = MagicMock()
        mock_task_service_class.return_value = mock_service
        
        # Mock tasks
        mock_task1 = MagicMock()
        mock_task1.__str__ = MagicMock(return_value="Task 1: Test Task (Active, medium priority)")
        mock_task2 = MagicMock()
        mock_task2.__str__ = MagicMock(return_value="Task 2: Another Task (Completed, high priority)")
        
        mock_service.get_all_tasks.return_value = [mock_task1, mock_task2]
        
        with patch('builtins.print') as mock_print:
            try:
                main()
            except SystemExit:
                pass
            
            mock_service.get_all_tasks.assert_called_once_with(show_completed=False)

    @patch('src.cli.TaskService')
    @patch('sys.argv', ['cli.py', 'list', '-a'])
    def test_list_all_tasks(self, mock_task_service_class):
        """Test listing all tasks including completed via CLI."""
        mock_service = MagicMock()
        mock_task_service_class.return_value = mock_service
        mock_service.get_all_tasks.return_value = []
        
        with patch('builtins.print'):
            try:
                main()
            except SystemExit:
                pass
            
            mock_service.get_all_tasks.assert_called_once_with(show_completed=True)

    @patch('src.cli.TaskService')
    @patch('sys.argv', ['cli.py', 'complete', '1'])
    def test_complete_task(self, mock_task_service_class):
        """Test completing a task via CLI."""
        mock_service = MagicMock()
        mock_task_service_class.return_value = mock_service
        
        mock_task = MagicMock()
        mock_task.title = "Completed Task"
        mock_service.complete_task.return_value = mock_task
        
        with patch('builtins.print') as mock_print:
            try:
                main()
            except SystemExit:
                pass
            
            mock_service.complete_task.assert_called_once_with(1)

    @patch('src.cli.TaskService')
    @patch('sys.argv', ['cli.py', 'delete', '1'])
    def test_delete_task(self, mock_task_service_class):
        """Test deleting a task via CLI."""
        mock_service = MagicMock()
        mock_task_service_class.return_value = mock_service
        
        mock_task = MagicMock()
        mock_task.title = "Deleted Task"
        mock_service.delete_task.return_value = mock_task
        
        with patch('builtins.print') as mock_print:
            try:
                main()
            except SystemExit:
                pass
            
            mock_service.delete_task.assert_called_once_with(1)

    @patch('src.cli.TaskService')
    @patch('sys.argv', ['cli.py', 'search', 'keyword'])
    def test_search_tasks(self, mock_task_service_class):
        """Test searching tasks via CLI."""
        mock_service = MagicMock()
        mock_task_service_class.return_value = mock_service
        
        mock_task = MagicMock()
        mock_task.__str__ = MagicMock(return_value="Task 1: Found Task (Active, medium priority)")
        mock_service.search_tasks.return_value = [mock_task]
        
        with patch('builtins.print') as mock_print:
            try:
                main()
            except SystemExit:
                pass
            
            mock_service.search_tasks.assert_called_once_with("keyword")

    @patch('src.cli.TaskService')
    @patch('sys.argv', ['cli.py', 'view', '1'])
    def test_view_task(self, mock_task_service_class):
        """Test viewing a specific task via CLI."""
        mock_service = MagicMock()
        mock_task_service_class.return_value = mock_service
        
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task.description = "Test Description"
        mock_task.priority = "high"
        mock_task.completed = False
        mock_task.created_at = "2023-01-01 10:00:00"
        
        mock_service.get_task_by_id.return_value = mock_task
        
        with patch('builtins.print') as mock_print:
            try:
                main()
            except SystemExit:
                pass
            
            mock_service.get_task_by_id.assert_called_once_with(1)

    @patch('src.cli.TaskService')
    @patch('sys.argv', ['cli.py', 'complete', '999'])
    def test_complete_nonexistent_task(self, mock_task_service_class):
        """Test completing a non-existent task via CLI."""
        from src.utils.exceptions import TaskNotFoundException
        
        mock_service = MagicMock()
        mock_task_service_class.return_value = mock_service
        mock_service.complete_task.side_effect = TaskNotFoundException("Task with ID 999 not found")
        
        with patch('builtins.print') as mock_print:
            try:
                main()
            except SystemExit:
                pass
            
            # Should print error message
            mock_print.assert_called()

    @patch('src.cli.TaskService')
    @patch('sys.argv', ['cli.py', 'view', '999'])
    def test_view_nonexistent_task(self, mock_task_service_class):
        """Test viewing a non-existent task via CLI."""
        from src.utils.exceptions import TaskNotFoundException
        
        mock_service = MagicMock()
        mock_task_service_class.return_value = mock_service
        mock_service.get_task_by_id.side_effect = TaskNotFoundException("Task with ID 999 not found")
        
        with patch('builtins.print') as mock_print:
            try:
                main()
            except SystemExit:
                pass
            
            # Should print error message
            mock_print.assert_called()

    @patch('sys.argv', ['cli.py', '--help'])
    def test_help_command(self):
        """Test that help command works."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        # argparse exits with code 0 for help
        assert exc_info.value.code == 0

    @patch('sys.argv', ['cli.py'])
    def test_no_command(self):
        """Test behavior when no command is provided."""
        with pytest.raises(SystemExit):
            main()

    @patch('sys.argv', ['cli.py', 'invalid_command'])
    def test_invalid_command(self):
        """Test behavior with invalid command."""
        with pytest.raises(SystemExit):
            main()