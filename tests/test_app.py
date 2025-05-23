"""
Tests for the Streamlit web application.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock streamlit before importing app
sys.modules['streamlit'] = MagicMock()
import streamlit as st

from src.app import display_tasks_page, add_task_page, search_tasks_page
from src.models.task import Task


class TestApp(unittest.TestCase):
    """Test cases for the Streamlit web application."""

    def setUp(self):
        """Set up test fixtures."""
        # Reset mocks
        st.reset_mock()
        
        # Create a mock task service
        self.mock_task_service = MagicMock()
        
        # Create some mock tasks
        self.task1 = Task(1, "Task 1", "Description 1", "low", False, "2023-01-01 12:00:00")
        self.task2 = Task(2, "Task 2", "Description 2", "medium", False, "2023-01-02 12:00:00")
        self.task3 = Task(3, "Task 3", "Description 3", "high", True, "2023-01-03 12:00:00")

    def test_display_tasks_page(self):
        """Test the display_tasks_page function."""
        # Setup mock return values
        self.mock_task_service.get_all_tasks.return_value = [self.task1, self.task2, self.task3]
        
        # Mock checkbox and selectbox
        st.checkbox.return_value = False
        st.selectbox.return_value = "All"
        
        # Mock columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        st.columns.return_value = [mock_col1, mock_col2, mock_col3]
        
        # Call the function
        display_tasks_page(self.mock_task_service)
        
        # Verify the task service was called correctly
        self.mock_task_service.get_all_tasks.assert_called_once_with(show_completed=True)
        
        # Verify streamlit components were used
        st.header.assert_called_once_with("Your Tasks")
        st.checkbox.assert_called_once_with("Show completed tasks", value=False)
        st.selectbox.assert_called_once()
        st.columns.assert_called()
        
        # Since we mocked show_completed=False, only active tasks should be displayed
        self.assertEqual(st.container.call_count, 2)  # Only task1 and task2

    def test_display_tasks_page_with_no_tasks(self):
        """Test the display_tasks_page function with no tasks."""
        # Setup mock return values
        self.mock_task_service.get_all_tasks.return_value = []
        
        # Call the function
        display_tasks_page(self.mock_task_service)
        
        # Verify the info message was displayed
        st.info.assert_called_once_with("No tasks found matching your criteria.")

    def test_add_task_page(self):
        """Test the add_task_page function."""
        # Setup mock form inputs
        mock_form = MagicMock()
        st.form.return_value.__enter__.return_value = mock_form
        mock_form.text_input.return_value = "New Task"
        mock_form.text_area.return_value = "New Description"
        mock_form.select_slider.return_value = "High"
        mock_form.form_submit_button.return_value = True
        
        # Setup mock task service
        new_task = Task(1, "New Task", "New Description", "high")
        self.mock_task_service.add_task.return_value = new_task
        
        # Call the function
        add_task_page(self.mock_task_service)
        
        # Verify the task service was called correctly
        self.mock_task_service.add_task.assert_called_once_with(
            title="New Task",
            description="New Description",
            priority="high"
        )
        
        # Verify success message was displayed
        st.success.assert_called_once_with("Task 'New Task' added successfully with ID 1")

    def test_add_task_page_with_empty_title(self):
        """Test the add_task_page function with an empty title."""
        # Setup mock form inputs
        mock_form = MagicMock()
        st.form.return_value.__enter__.return_value = mock_form
        mock_form.text_input.return_value = ""  # Empty title
        mock_form.text_area.return_value = "New Description"
        mock_form.select_slider.return_value = "High"
        mock_form.form_submit_button.return_value = True
        
        # Call the function
        add_task_page(self.mock_task_service)
        
        # Verify error message was displayed
        st.error.assert_called_once_with("Title is required")
        
        # Verify task service was not called
        self.mock_task_service.add_task.assert_not_called()

    def test_search_tasks_page(self):
        """Test the search_tasks_page function."""
        # Setup mock text input
        st.text_input.return_value = "Task"
        
        # Setup mock task service
        self.mock_task_service.search_tasks.return_value = [self.task1, self.task2]
        
        # Call the function
        search_tasks_page(self.mock_task_service)
        
        # Verify the task service was called correctly
        self.mock_task_service.search_tasks.assert_called_once_with("Task")
        
        # Verify search results were displayed
        st.write.assert_any_call("Found 2 tasks matching 'Task':")
        
        # Verify containers were created for each task
        self.assertEqual(st.container.call_count, 2)

    def test_search_tasks_page_with_no_results(self):
        """Test the search_tasks_page function with no results."""
        # Setup mock text input
        st.text_input.return_value = "Nonexistent"
        
        # Setup mock task service
        self.mock_task_service.search_tasks.return_value = []
        
        # Call the function
        search_tasks_page(self.mock_task_service)
        
        # Verify the task service was called correctly
        self.mock_task_service.search_tasks.assert_called_once_with("Nonexistent")
        
        # Verify info message was displayed
        st.info.assert_called_once_with("No tasks found matching 'Nonexistent'")

    @patch("src.app.hasattr")
    def test_search_tasks_page_with_task_to_view(self, mock_hasattr):
        """Test the search_tasks_page function with a task to view."""
        # Setup mock text input
        st.text_input.return_value = "Task"
        
        # Setup mock task service
        self.mock_task_service.search_tasks.return_value = [self.task1]
        
        # Setup session state with task_to_view
        mock_hasattr.return_value = True
        st.session_state.task_to_view = 1
        self.mock_task_service.get_task_by_id.return_value = self.task1
        
        # Call the function
        search_tasks_page(self.mock_task_service)
        
        # Verify the task service was called correctly
        self.mock_task_service.get_task_by_id.assert_called_once_with(1)
        
        # Verify task details were displayed
        st.subheader.assert_called_once_with("Task Details: Task 1")
        st.write.assert_any_call("**ID:** 1")
        st.write.assert_any_call("**Description:** Description 1")
        st.write.assert_any_call("**Priority:** low")
        st.write.assert_any_call("**Status:** Active")
        st.write.assert_any_call("**Created at:** 2023-01-01 12:00:00")


if __name__ == "__main__":
    unittest.main()