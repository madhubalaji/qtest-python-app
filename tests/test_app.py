"""
Tests for the Streamlit web application.
"""

import unittest
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.task_service import TaskService
from src.models.task import Task


class TestAppFunctions(unittest.TestCase):
    """Test cases for the app functions."""

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
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_delete_task_button(self, mock_rerun, mock_success, mock_button):
        """Test that clicking the delete button deletes the task."""
        # Import here to avoid Streamlit initialization during test collection
        from src.app import display_tasks_page
        
        # Mock the button click
        mock_button.return_value = True
        
        # Call the function with our task service
        with patch('streamlit.columns') as mock_columns:
            # Mock the columns structure
            mock_col1 = MagicMock()
            mock_col2 = MagicMock()
            mock_col3 = MagicMock()
            mock_col3_1 = MagicMock()
            mock_col3_2 = MagicMock()
            
            mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
            mock_col3.columns.return_value = [mock_col3_1, mock_col3_2]
            
            # This will simulate clicking the delete button
            display_tasks_page(self.task_service)
            
            # Check that the success message was shown
            mock_success.assert_called_once()
            
            # Check that the page was rerun
            mock_rerun.assert_called_once()
            
            # Check that the task was deleted
            tasks = self.task_service.get_all_tasks()
            self.assertEqual(len(tasks), 2)  # One task should be deleted

    @patch('streamlit.button')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_delete_task_in_search_view(self, mock_rerun, mock_success, mock_button):
        """Test that clicking the delete button in search view deletes the task."""
        # Import here to avoid Streamlit initialization during test collection
        from src.app import search_tasks_page
        
        # Mock the button click for "Delete Task"
        mock_button.return_value = True
        
        # Set up session state with a task to view
        import streamlit as st
        st.session_state = {}
        st.session_state["task_to_view"] = self.task1.id
        
        # Call the function with our task service
        with patch('streamlit.columns') as mock_columns:
            # Mock the columns structure
            mock_col1 = MagicMock()
            mock_col2 = MagicMock()
            
            mock_columns.return_value = [mock_col1, mock_col2, MagicMock()]
            
            # This will simulate clicking the delete button
            search_tasks_page(self.task_service)
            
            # Check that the success message was shown
            mock_success.assert_called_once()
            
            # Check that the page was rerun
            mock_rerun.assert_called_once()
            
            # Check that the task was deleted
            tasks = self.task_service.get_all_tasks()
            self.assertEqual(len(tasks), 2)  # One task should be deleted


if __name__ == "__main__":
    unittest.main()