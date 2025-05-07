"""
Tests for the Streamlit app functionality.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.app import display_tasks_page, add_task_page, search_tasks_page
from src.services.task_service import TaskService
from src.models.task import Task


class TestAppFunctionality(unittest.TestCase):
    """Test cases for the Streamlit app functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.task_service = MagicMock(spec=TaskService)
        # Create some sample tasks for testing
        self.sample_tasks = [
            Task(1, "Task 1", "Description 1", "high", False),
            Task(2, "Task 2", "Description 2", "medium", True),
            Task(3, "Task 3", "Description 3", "low", False)
        ]

    @patch('streamlit.container')
    @patch('streamlit.columns')
    @patch('streamlit.expander')
    def test_display_tasks_page(self, mock_expander, mock_columns, mock_container):
        """Test the display_tasks_page function."""
        # Setup mock returns
        self.task_service.get_all_tasks.return_value = self.sample_tasks
        
        # Mock columns to return MagicMock objects
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
        
        # Call the function
        display_tasks_page(self.task_service)
        
        # Assert that the task service was called correctly
        self.task_service.get_all_tasks.assert_called_once()

    @patch('streamlit.form')
    def test_add_task_page(self, mock_form):
        """Test the add_task_page function."""
        # Setup mock form
        mock_form_obj = MagicMock()
        mock_form.return_value.__enter__.return_value = mock_form_obj
        mock_form_obj.form_submit_button.return_value = True
        
        # Setup mock input values
        with patch('streamlit.text_input', return_value="New Task"):
            with patch('streamlit.text_area', return_value="New Description"):
                with patch('streamlit.selectbox', return_value="high"):
                    # Call the function
                    add_task_page(self.task_service)
                    
                    # Assert that the task service was called correctly
                    self.task_service.add_task.assert_called_once_with(
                        "New Task", "New Description", "high"
                    )

    @patch('streamlit.text_input')
    @patch('streamlit.container')
    @patch('streamlit.columns')
    def test_search_tasks_page(self, mock_columns, mock_container, mock_text_input):
        """Test the search_tasks_page function."""
        # Setup mock returns
        mock_text_input.return_value = "test"
        self.task_service.search_tasks.return_value = [self.sample_tasks[0]]
        
        # Mock columns to return MagicMock objects
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        # Call the function
        search_tasks_page(self.task_service)
        
        # Assert that the task service was called correctly
        self.task_service.search_tasks.assert_called_once_with("test")


if __name__ == "__main__":
    unittest.main()