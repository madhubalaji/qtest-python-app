"""
Tests for the Streamlit app functionality.
"""

import pytest
from unittest.mock import MagicMock
import streamlit as st
from unittest.mock import Mock, patch

from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestAppFunctionality:
    """Test class for app functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_tasks = [
            Mock(
                id=1,
                title="Test Task 1",
                description="Test Description 1",
                priority="high",
                completed=False,
                created_at="2023-01-01 10:00:00"
            ),
            Mock(
                id=2,
                title="Test Task 2",
                description="Test Description 2",
                priority="medium",
                completed=True,
                created_at="2023-01-02 11:00:00"
            )
        ]

    @patch('streamlit.button')
    @patch('streamlit.rerun')
    def test_complete_button_functionality(self, mock_rerun, mock_button):
        """Test the complete button functionality."""
        # Mock the button to return True (clicked)
        mock_button.return_value = True

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [self.mock_tasks[0]]  # Only incomplete task

        # Import and test the display function
        from src.app import display_tasks_page

        with patch('streamlit.header'), \
             patch('streamlit.columns', return_value=[Mock(), Mock(), Mock(), Mock()]), \
             patch('streamlit.checkbox'), \
             patch('streamlit.selectbox'), \
             patch('streamlit.container'), \
             patch('streamlit.markdown'), \
             patch('streamlit.expander'), \
             patch('streamlit.write'), \
             patch('streamlit.divider'):

            display_tasks_page(mock_task_service)

        # Verify complete_task was called
        mock_task_service.complete_task.assert_called_once_with(1)
        mock_rerun.assert_called_once()

    @patch('streamlit.button')
    @patch('streamlit.rerun')
    def test_delete_button_functionality(self, mock_rerun, mock_button):
        """Test the delete button functionality."""
        # Mock the button to return True (clicked) for delete button
        def button_side_effect(*args, **kwargs):
            if 'delete_' in kwargs.get('key', ''):
                return True
            return False

        mock_button.side_effect = button_side_effect

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.get_all_tasks.return_value = [self.mock_tasks[0]]  # Only one task

        # Import and test the display function
        from src.app import display_tasks_page

        with patch('streamlit.header'), \
             patch('streamlit.columns', return_value=[Mock(), Mock(), Mock(), Mock()]), \
             patch('streamlit.checkbox'), \
             patch('streamlit.selectbox'), \
             patch('streamlit.container'), \
             patch('streamlit.markdown'), \
             patch('streamlit.expander'), \
             patch('streamlit.write'), \
             patch('streamlit.divider'):

            display_tasks_page(mock_task_service)

        # Verify delete_task was called
        mock_task_service.delete_task.assert_called_once_with(1)
        mock_rerun.assert_called_once()

    @patch('streamlit.button')
    @patch('streamlit.rerun')
    def test_search_page_view_button(self, mock_rerun, mock_button):
        """Test the view button in search page."""
        mock_button.return_value = True

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.search_tasks.return_value = [self.mock_tasks[0]]

        # Import and test the search function
        from src.app import search_tasks_page

        with patch('streamlit.header'), \
             patch('streamlit.text_input', return_value='test'), \
             patch('streamlit.write'), \
             patch('streamlit.container'), \
             patch('streamlit.columns', return_value=[Mock(), Mock()]), \
             patch('streamlit.markdown'), \
             patch('streamlit.expander'), \
             patch('streamlit.divider'), \
             patch('streamlit.session_state', {}) as mock_session_state:

            search_tasks_page(mock_task_service)

        # Verify session state was set
        assert mock_session_state['task_to_view'] == 1
        mock_rerun.assert_called_once()

    @patch('streamlit.button')
    @patch('streamlit.rerun')
    def test_task_detail_delete_button(self, mock_rerun, mock_button):
        """Test the delete button in task detail view."""
        # Mock buttons - delete button returns True
        def button_side_effect(text, **kwargs):
            if text == "Delete Task":
                return True
            return False

        mock_button.side_effect = button_side_effect

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.get_task_by_id.return_value = self.mock_tasks[0]

        # Import and test the search function with task detail view
        from src.app import search_tasks_page

        with patch('streamlit.header'), \
             patch('streamlit.text_input', return_value='test'), \
             patch('streamlit.write'), \
             patch('streamlit.container'), \
             patch('streamlit.columns', return_value=[Mock(), Mock(), Mock()]), \
             patch('streamlit.markdown'), \
             patch('streamlit.expander'), \
             patch('streamlit.divider'), \
             patch('streamlit.subheader'), \
             patch('streamlit.session_state', {'task_to_view': 1}) as mock_session_state:

            search_tasks_page(mock_task_service)

        # Verify delete_task was called and session state was cleared
        mock_task_service.delete_task.assert_called_once_with(1)
        assert 'task_to_view' not in mock_session_state
        mock_rerun.assert_called_once()

    @patch('streamlit.button')
    @patch('streamlit.rerun')
    def test_task_detail_complete_button(self, mock_rerun, mock_button):
        """Test the complete button in task detail view."""
        # Mock buttons - complete button returns True
        def button_side_effect(text, **kwargs):
            if text == "Mark as Complete":
                return True
            return False

        mock_button.side_effect = button_side_effect

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.get_task_by_id.return_value = self.mock_tasks[0]  # Incomplete task

        # Import and test the search function with task detail view
        from src.app import search_tasks_page

        with patch('streamlit.header'), \
             patch('streamlit.text_input', return_value='test'), \
             patch('streamlit.write'), \
             patch('streamlit.container'), \
             patch('streamlit.columns', return_value=[Mock(), Mock(), Mock()]), \
             patch('streamlit.markdown'), \
             patch('streamlit.expander'), \
             patch('streamlit.divider'), \
             patch('streamlit.subheader'), \
             patch('streamlit.session_state', {'task_to_view': 1}):

            search_tasks_page(mock_task_service)

        # Verify complete_task was called
        mock_task_service.complete_task.assert_called_once_with(1)
        mock_rerun.assert_called_once()

    @patch('streamlit.button')
    @patch('streamlit.rerun')
    def test_task_detail_close_button(self, mock_rerun, mock_button):
        """Test the close button in task detail view."""
        # Mock buttons - close button returns True
        def button_side_effect(text, **kwargs):
            if text == "Close":
                return True
            return False

        mock_button.side_effect = button_side_effect

        # Mock task service
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.get_task_by_id.return_value = self.mock_tasks[0]

        # Import and test the search function with task detail view
        from src.app import search_tasks_page

        with patch('streamlit.header'), \
             patch('streamlit.text_input', return_value='test'), \
             patch('streamlit.write'), \
             patch('streamlit.container'), \
             patch('streamlit.columns', return_value=[Mock(), Mock(), Mock()]), \
             patch('streamlit.markdown'), \
             patch('streamlit.expander'), \
             patch('streamlit.divider'), \
             patch('streamlit.subheader'), \
             patch('streamlit.session_state', {'task_to_view': 1}) as mock_session_state:

            search_tasks_page(mock_task_service)

        # Verify session state was cleared
        assert 'task_to_view' not in mock_session_state
        mock_rerun.assert_called_once()

    def test_task_not_found_handling(self):
        """Test handling of TaskNotFoundException in task detail view."""
        # Mock task service to raise exception
        mock_task_service = Mock(spec=TaskService)
        mock_task_service.get_task_by_id.side_effect = TaskNotFoundException("Task not found")

        # Import and test the search function with task detail view
        from src.app import search_tasks_page

        with patch('streamlit.header'), \
             patch('streamlit.text_input', return_value='test'), \
             patch('streamlit.write'), \
             patch('streamlit.container'), \
             patch('streamlit.columns', return_value=[Mock(), Mock()]), \
             patch('streamlit.markdown'), \
             patch('streamlit.expander'), \
             patch('streamlit.divider'), \
             patch('streamlit.error') as mock_error, \
             patch('streamlit.session_state', {'task_to_view': 999}) as mock_session_state:

            search_tasks_page(mock_task_service)

        # Verify error was displayed and session state was cleared
        mock_error.assert_called_once_with("Task not found")
        assert 'task_to_view' not in mock_session_state