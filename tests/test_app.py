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

    @patch('streamlit.container')
    @patch('streamlit.expander')
    @patch('streamlit.write')
    @patch('streamlit.markdown')
    @patch('streamlit.info')
    @patch('streamlit.selectbox')
    @patch('streamlit.checkbox')
    @patch('streamlit.header')
    @patch('streamlit.rerun')
    @patch('streamlit.success')
    @patch('streamlit.button')
    def test_delete_task_button(self, mock_button, mock_success, mock_rerun, mock_header,
                             mock_checkbox, mock_selectbox, mock_info, mock_markdown,
                             mock_write, mock_expander, mock_container):
        """Test that clicking the delete button deletes the task."""
        # Import here to avoid Streamlit initialization during test collection
        from src.app import display_tasks_page
        
        # Setup default mock returns
        mock_checkbox.return_value = False
        mock_selectbox.return_value = "All"
        mock_container.return_value.__enter__.return_value = MagicMock()
        mock_container.return_value.__exit__.return_value = None
        mock_expander.return_value.__enter__.return_value = MagicMock()
        mock_expander.return_value.__exit__.return_value = None

        # Mock the columns
        with patch('streamlit.columns') as mock_columns:
            # Mock column objects
            mock_col1 = MagicMock()
            mock_col2 = MagicMock()
            mock_col3 = MagicMock()
            mock_action_col1 = MagicMock()
            mock_action_col2 = MagicMock()

            def column_side_effect(*args):
                if not args:
                    return [mock_col1, mock_col2]
                if args[0] == 3 or args[0] == [3, 1, 1]:
                    return [mock_col1, mock_col2, mock_col3]
                if args[0] == 2:
                    return [mock_action_col1, mock_action_col2]
                return [mock_col1, mock_col2]

            mock_columns.side_effect = column_side_effect

            # Mock button behavior
            def button_side_effect(*args, **kwargs):
                if 'key' in kwargs and kwargs['key'].startswith('delete_'):
                    return True
                return False

            mock_button.side_effect = button_side_effect

            # Run the function
            display_tasks_page(self.task_service)

            # Verify the results
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()
            tasks = self.task_service.get_all_tasks()
            self.assertEqual(len(tasks), 2)  # One task should be deleted

    @patch('streamlit.container')
    @patch('streamlit.write')
    @patch('streamlit.markdown')
    @patch('streamlit.text_input')
    @patch('streamlit.header')
    @patch('streamlit.rerun')
    @patch('streamlit.success')
    @patch('streamlit.button')
    @patch('streamlit.subheader')
    def test_delete_task_in_search_view(self, mock_subheader, mock_button, mock_success, mock_rerun,
                                    mock_header, mock_text_input, mock_markdown,
                                    mock_write, mock_container):
        """Test that clicking the delete button in search view deletes the task."""
        # Import here to avoid Streamlit initialization during test collection
        from src.app import search_tasks_page

        # Setup container mock
        mock_container.return_value.__enter__.return_value = MagicMock()
        mock_container.return_value.__exit__.return_value = None

        # Set up the session state
        import streamlit as st
        st.session_state = {}
        st.session_state["task_to_view"] = self.task1.id

        # Mock the columns
        with patch('streamlit.columns') as mock_columns:
            # Mock column objects
            mock_col1 = MagicMock()
            mock_col2 = MagicMock()
            mock_col3 = MagicMock()

            def column_side_effect(*args):
                if args[0] == 3:
                    return [mock_col1, mock_col2, mock_col3]
                return [mock_col1, mock_col2]

            mock_columns.side_effect = column_side_effect

            # Mock button behavior
            def button_side_effect(*args, **kwargs):
                if args and args[0] == "Delete Task":
                    return True
                return False

            mock_button.side_effect = button_side_effect

            # Run the function
            search_tasks_page(self.task_service)

            # Verify the results
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()
            tasks = self.task_service.get_all_tasks()
            self.assertEqual(len(tasks), 2)  # One task should be deleted


if __name__ == "__main__":
    unittest.main()