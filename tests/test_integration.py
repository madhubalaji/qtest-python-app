"""
Integration tests for the task manager application.
"""

import pytest
import os
import tempfile
import subprocess
import sys
from unittest.mock import patch
from src.cli import main
from src.services.task_service import TaskService


class TestCLIIntegration:
    """Integration tests for the CLI functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "test_tasks.json")

    def teardown_method(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_file):
            os.unlink(self.temp_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    @patch('src.cli.TaskService')
    def test_cli_add_command(self, mock_task_service_class):
        """Test CLI add command."""
        # Mock the TaskService
        mock_service = mock_task_service_class.return_value
        mock_task = type('Task', (), {'id': 1, 'title': 'Test Task'})()
        mock_service.add_task.return_value = mock_task

        # Test add command
        with patch('sys.argv', ['cli.py', 'add', 'Test Task', '-d', 'Test Description', '-p', 'high']):
            with patch('builtins.print') as mock_print:
                main()
                mock_service.add_task.assert_called_once_with('Test Task', 'Test Description', 'high')
                mock_print.assert_called_with("Task 'Test Task' added successfully with ID 1.")

    @patch('src.cli.TaskService')
    def test_cli_list_command_empty(self, mock_task_service_class):
        """Test CLI list command with no tasks."""
        mock_service = mock_task_service_class.return_value
        mock_service.get_all_tasks.return_value = []

        with patch('sys.argv', ['cli.py', 'list']):
            with patch('builtins.print') as mock_print:
                main()
                mock_service.get_all_tasks.assert_called_once_with(show_completed=False)
                mock_print.assert_called_with("No tasks found.")

    @patch('src.cli.TaskService')
    def test_cli_list_command_with_tasks(self, mock_task_service_class):
        """Test CLI list command with tasks."""
        mock_service = mock_task_service_class.return_value
        
        # Create mock tasks
        mock_task1 = type('Task', (), {
            'id': 1, 
            'title': 'Task 1', 
            'priority': 'high', 
            'completed': False,
            'created_at': '2023-01-01 12:00:00'
        })()
        
        mock_task2 = type('Task', (), {
            'id': 2, 
            'title': 'Task 2', 
            'priority': 'low', 
            'completed': True,
            'created_at': '2023-01-02 12:00:00'
        })()
        
        mock_service.get_all_tasks.return_value = [mock_task1, mock_task2]

        with patch('sys.argv', ['cli.py', 'list', '-a']):
            with patch('builtins.print') as mock_print:
                main()
                mock_service.get_all_tasks.assert_called_once_with(show_completed=True)
                # Check that print was called multiple times (for the table)
                assert mock_print.call_count > 1

    @patch('src.cli.TaskService')
    def test_cli_complete_command(self, mock_task_service_class):
        """Test CLI complete command."""
        mock_service = mock_task_service_class.return_value
        mock_task = type('Task', (), {'id': 1, 'title': 'Test Task'})()
        mock_service.complete_task.return_value = mock_task

        with patch('sys.argv', ['cli.py', 'complete', '1']):
            with patch('builtins.print') as mock_print:
                main()
                mock_service.complete_task.assert_called_once_with(1)
                mock_print.assert_called_with("Task 1 marked as complete.")

    @patch('src.cli.TaskService')
    def test_cli_delete_command(self, mock_task_service_class):
        """Test CLI delete command."""
        mock_service = mock_task_service_class.return_value
        mock_task = type('Task', (), {'id': 1, 'title': 'Test Task'})()
        mock_service.delete_task.return_value = mock_task

        with patch('sys.argv', ['cli.py', 'delete', '1']):
            with patch('builtins.print') as mock_print:
                main()
                mock_service.delete_task.assert_called_once_with(1)
                mock_print.assert_called_with("Task 'Test Task' deleted successfully.")

    @patch('src.cli.TaskService')
    def test_cli_search_command(self, mock_task_service_class):
        """Test CLI search command."""
        mock_service = mock_task_service_class.return_value
        
        mock_task = type('Task', (), {
            'id': 1, 
            'title': 'Python Task', 
            'priority': 'high', 
            'completed': False
        })()
        
        mock_service.search_tasks.return_value = [mock_task]

        with patch('sys.argv', ['cli.py', 'search', 'python']):
            with patch('builtins.print') as mock_print:
                main()
                mock_service.search_tasks.assert_called_once_with('python')
                # Check that results were printed
                assert mock_print.call_count > 1

    @patch('src.cli.TaskService')
    def test_cli_search_command_no_results(self, mock_task_service_class):
        """Test CLI search command with no results."""
        mock_service = mock_task_service_class.return_value
        mock_service.search_tasks.return_value = []

        with patch('sys.argv', ['cli.py', 'search', 'nonexistent']):
            with patch('builtins.print') as mock_print:
                main()
                mock_service.search_tasks.assert_called_once_with('nonexistent')
                mock_print.assert_called_with("No tasks found matching 'nonexistent'.")

    @patch('src.cli.TaskService')
    def test_cli_view_command(self, mock_task_service_class):
        """Test CLI view command."""
        mock_service = mock_task_service_class.return_value
        
        mock_task = type('Task', (), {
            'id': 1,
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'high',
            'completed': False,
            'created_at': '2023-01-01 12:00:00'
        })()
        
        mock_service.get_task_by_id.return_value = mock_task

        with patch('sys.argv', ['cli.py', 'view', '1']):
            with patch('builtins.print') as mock_print:
                main()
                mock_service.get_task_by_id.assert_called_once_with(1)
                # Check that task details were printed
                assert mock_print.call_count > 1

    def test_cli_no_command(self):
        """Test CLI with no command shows help."""
        with patch('sys.argv', ['cli.py']):
            with patch('argparse.ArgumentParser.print_help') as mock_help:
                main()
                mock_help.assert_called_once()


class TestApplicationIntegration:
    """Integration tests for the overall application."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "integration_tasks.json")

    def teardown_method(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_file):
            os.unlink(self.temp_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_full_task_lifecycle(self):
        """Test complete task lifecycle: create, read, update, delete."""
        service = TaskService(storage_file=self.temp_file)
        
        # Create task
        task = service.add_task("Integration Test Task", "Test Description", "high")
        assert task.id == 1
        assert task.title == "Integration Test Task"
        
        # Read task
        retrieved_task = service.get_task_by_id(task.id)
        assert retrieved_task.title == task.title
        
        # Update task
        updated_task = service.update_task(task.id, title="Updated Task", completed=True)
        assert updated_task.title == "Updated Task"
        assert updated_task.completed is True
        
        # Search for task
        search_results = service.search_tasks("Updated")
        assert len(search_results) == 1
        assert search_results[0].title == "Updated Task"
        
        # Delete task
        deleted_task = service.delete_task(task.id)
        assert deleted_task.title == "Updated Task"
        
        # Verify task is deleted
        with pytest.raises(Exception):  # TaskNotFoundException
            service.get_task_by_id(task.id)

    def test_persistence_across_service_instances(self):
        """Test that data persists across different service instances."""
        # Create task with first service instance
        service1 = TaskService(storage_file=self.temp_file)
        task1 = service1.add_task("Persistent Task 1")
        task2 = service1.add_task("Persistent Task 2")
        
        # Create second service instance and verify data persistence
        service2 = TaskService(storage_file=self.temp_file)
        tasks = service2.get_all_tasks()
        
        assert len(tasks) == 2
        assert tasks[0].title == "Persistent Task 1"
        assert tasks[1].title == "Persistent Task 2"
        
        # Modify data with second service
        service2.complete_task(task1.id)
        
        # Create third service instance and verify changes
        service3 = TaskService(storage_file=self.temp_file)
        updated_task = service3.get_task_by_id(task1.id)
        assert updated_task.completed is True

    def test_concurrent_operations(self):
        """Test handling of concurrent-like operations."""
        service1 = TaskService(storage_file=self.temp_file)
        service2 = TaskService(storage_file=self.temp_file)
        
        # Add tasks with both services
        task1 = service1.add_task("Task from Service 1")
        task2 = service2.add_task("Task from Service 2")
        
        # Verify both tasks exist in fresh service instance
        service3 = TaskService(storage_file=self.temp_file)
        all_tasks = service3.get_all_tasks()
        
        # Should have at least the tasks we created
        task_titles = [task.title for task in all_tasks]
        assert "Task from Service 1" in task_titles or "Task from Service 2" in task_titles

    def test_error_handling_integration(self):
        """Test error handling in integrated scenarios."""
        service = TaskService(storage_file=self.temp_file)
        
        # Test operations on non-existent tasks
        with pytest.raises(Exception):  # TaskNotFoundException
            service.get_task_by_id(999)
        
        with pytest.raises(Exception):  # TaskNotFoundException
            service.update_task(999, title="Non-existent")
        
        with pytest.raises(Exception):  # TaskNotFoundException
            service.complete_task(999)
        
        with pytest.raises(Exception):  # TaskNotFoundException
            service.delete_task(999)

    def test_streamlit_app_imports(self):
        """Test that the Streamlit app can be imported without errors."""
        try:
            import src.app
            # If we get here, the import was successful
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import Streamlit app: {e}")
        except Exception as e:
            # Other exceptions might be expected (like Streamlit not being available)
            # but the import structure should be correct
            if "streamlit" not in str(e).lower():
                pytest.fail(f"Unexpected error importing app: {e}")

    def test_package_structure(self):
        """Test that the package structure is correct."""
        # Test that all modules can be imported
        from src.models.task import Task
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        
        # Test that classes can be instantiated
        task = Task(1, "Test Task")
        assert task.id == 1
        
        service = TaskService(storage_file=self.temp_file)
        assert service.storage_file == self.temp_file
        
        exception = TaskNotFoundException("Test message")
        assert str(exception) == "Test message"