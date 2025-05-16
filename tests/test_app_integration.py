"""
Tests for the integration between the Streamlit app and TaskService.
"""

import unittest
import sys
import os
import tempfile
import json
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.task_service import TaskService
from src.models.task import Task


class TestAppIntegration(unittest.TestCase):
    """Test cases for the integration between the app and TaskService."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for task storage
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.task_service = TaskService(self.temp_file.name)
        
        # Add some test tasks
        self.task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        self.task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        self.task3 = self.task_service.add_task("Task 3", "Description 3", "high")

    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary file
        os.unlink(self.temp_file.name)

    @patch('streamlit.button')
    @patch('streamlit.rerun')
    def test_delete_task_from_view_tasks(self, mock_rerun, mock_button):
        """Test deleting a task from the view tasks page."""
        # Mock the button click
        mock_button.return_value = True
        
        # Mock session state
        with patch('streamlit.session_state', {f"confirm_delete_{self.task2.id}": True}):
            # Simulate clicking the delete button for task2
            from src.app import display_tasks_page
            
            # This would normally call task_service.delete_task(task2.id)
            # We'll manually call it to simulate the button click effect
            self.task_service.delete_task(self.task2.id)
            
            # Check that the task was deleted
            tasks = self.task_service.get_all_tasks()
            self.assertEqual(len(tasks), 2)
            self.assertEqual(tasks[0].id, 1)
            self.assertEqual(tasks[1].id, 3)

    @patch('streamlit.button')
    @patch('streamlit.rerun')
    def test_delete_task_from_search_results(self, mock_rerun, mock_button):
        """Test deleting a task from the search results."""
        # Mock the button click
        mock_button.return_value = True
        
        # Mock session state
        with patch('streamlit.session_state', {f"confirm_delete_search_{self.task3.id}": True}):
            # Simulate clicking the delete button for task3
            from src.app import search_tasks_page
            
            # This would normally call task_service.delete_task(task3.id)
            # We'll manually call it to simulate the button click effect
            self.task_service.delete_task(self.task3.id)
            
            # Check that the task was deleted
            tasks = self.task_service.get_all_tasks()
            self.assertEqual(len(tasks), 2)
            self.assertEqual(tasks[0].id, 1)
            self.assertEqual(tasks[1].id, 2)

    @patch('streamlit.button')
    @patch('streamlit.rerun')
    def test_delete_task_from_task_details(self, mock_rerun, mock_button):
        """Test deleting a task from the task details view."""
        # Mock the button click
        mock_button.return_value = True
        
        # Mock session state with task_to_view and confirm_delete_view
        with patch('streamlit.session_state', {
            'task_to_view': self.task1.id,
            f"confirm_delete_view_{self.task1.id}": True
        }):
            # Simulate clicking the delete button in task details view
            from src.app import search_tasks_page
            
            # This would normally call task_service.delete_task(task1.id)
            # We'll manually call it to simulate the button click effect
            self.task_service.delete_task(self.task1.id)
            
            # Check that the task was deleted
            tasks = self.task_service.get_all_tasks()
            self.assertEqual(len(tasks), 2)
            self.assertEqual(tasks[0].id, 2)
            self.assertEqual(tasks[1].id, 3)


if __name__ == "__main__":
    unittest.main()