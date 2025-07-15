"""
Tests for the Streamlit app module.
"""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock

import streamlit as st

from src.app import (
    main, 
    display_tasks_page, 
    add_task_page, 
    search_tasks_page
)
from src.services.task_service import TaskService
from src.models.task import Task


class TestApp(unittest.TestCase):
    """Test cases for the Streamlit app module."""

    def setUp(self):
        """Set up a temporary file for task storage and mock Streamlit."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Create a TaskService with the temp file
        self.task_service = TaskService(self.temp_file.name)
        
        # Mock Streamlit
        self.mock_st = MagicMock()
        self.st_patcher = patch.multiple(
            'streamlit',
            set_page_config=MagicMock(),
            title=MagicMock(),
            write=MagicMock(),
            sidebar=MagicMock(),
            header=MagicMock(),
            columns=MagicMock(),
            checkbox=MagicMock(),
            selectbox=MagicMock(),
            info=MagicMock(),
            container=MagicMock(),
            markdown=MagicMock(),
            expander=MagicMock(),
            button=MagicMock(),
            experimental_rerun=MagicMock(),
            divider=MagicMock(),
            form=MagicMock(),
            text_input=MagicMock(),
            text_area=MagicMock(),
            select_slider=MagicMock(),
            form_submit_button=MagicMock(),
            error=MagicMock(),
            success=MagicMock(),
            subheader=MagicMock(),
            session_state=MagicMock()
        )
        self.st_patcher.start()

    def tearDown(self):
        """Clean up the temporary file and restore Streamlit."""
        os.unlink(self.temp_file.name)
        self.st_patcher.stop()

    @patch('src.app.TaskService')
    @patch('src.app.os.path.join')
    @patch('src.app.os.makedirs')
    def test_main_function(self, mock_makedirs, mock_join, mock_task_service):
        """Test the main function of the app."""
        # Setup mocks
        mock_join.return_value = self.temp_file.name
        mock_task_service_instance = MagicMock()
        mock_task_service.return_value = mock_task_service_instance
        
        # Mock sidebar radio to select "View Tasks"
        st.sidebar.radio.return_value = "View Tasks"
        
        # Call the main function
        with patch('src.app.display_tasks_page') as mock_display_tasks:
            main()
            mock_display_tasks.assert_called_once_with(mock_task_service_instance)
        
        # Verify page config was set
        st.set_page_config.assert_called_once()
        st.title.assert_called_once_with("Task Manager")
        
        # Test with "Add Task" selection
        st.sidebar.radio.return_value = "Add Task"
        with patch('src.app.add_task_page') as mock_add_task:
            main()
            mock_add_task.assert_called_once_with(mock_task_service_instance)
        
        # Test with "Search Tasks" selection
        st.sidebar.radio.return_value = "Search Tasks"
        with patch('src.app.search_tasks_page') as mock_search_tasks:
            main()
            mock_search_tasks.assert_called_once_with(mock_task_service_instance)

    def test_display_tasks_page(self):
        """Test the display_tasks_page function."""
        # Create some test tasks
        task1 = self.task_service.add_task("Task 1", "Description 1", "low")
        task2 = self.task_service.add_task("Task 2", "Description 2", "medium")
        task3 = self.task_service.add_task("Task 3", "Description 3", "high")
        self.task_service.complete_task(task2.id)
        
        # Mock the checkbox and selectbox returns
        st.checkbox.return_value = False  # Don't show completed tasks
        st.selectbox.return_value = "All"  # Don't filter by priority
        
        # Mock columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        st.columns.return_value = [mock_col1, mock_col2, mock_col3]
        
        # Mock container context manager
        mock_container = MagicMock()
        st.container.return_value.__enter__.return_value = mock_container
        
        # Call the function
        display_tasks_page(self.task_service)
        
        # Verify the header was set
        st.header.assert_called_with("Your Tasks")
        
        # Verify checkbox and selectbox were called
        st.checkbox.assert_called_with("Show completed tasks", value=False)
        st.selectbox.assert_called_with(
            "Filter by priority",
            ["All", "Low", "Medium", "High"]
        )

    def test_add_task_page(self):
        """Test the add_task_page function."""
        # Mock form context manager
        mock_form = MagicMock()
        st.form.return_value.__enter__.return_value = mock_form
        
        # Mock form inputs
        st.text_input.return_value = "New Task"
        st.text_area.return_value = "New Description"
        st.select_slider.return_value = "Medium"
        st.form_submit_button.return_value = True  # Form was submitted
        
        # Call the function
        add_task_page(self.task_service)
        
        # Verify the header was set
        st.header.assert_called_with("Add New Task")
        
        # Verify form inputs were called
        st.text_input.assert_called_with("Title", max_chars=50)
        st.text_area.assert_called_with("Description", max_chars=200)
        st.select_slider.assert_called_with(
            "Priority",
            options=["Low", "Medium", "High"],
            value="Medium"
        )
        
        # Verify success message was shown
        st.success.assert_called_once()
        
        # Verify a task was added
        tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "New Task")
        self.assertEqual(tasks[0].description, "New Description")
        self.assertEqual(tasks[0].priority, "medium")

    def test_search_tasks_page(self):
        """Test the search_tasks_page function."""
        # Create some test tasks
        self.task_service.add_task("Buy groceries", "Get milk and eggs")
        self.task_service.add_task("Clean house", "Vacuum and dust")
        self.task_service.add_task("Buy milk", "Get whole milk")
        
        # Mock text input
        st.text_input.return_value = "milk"
        
        # Mock container context manager
        mock_container = MagicMock()
        st.container.return_value.__enter__.return_value = mock_container
        
        # Mock columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        st.columns.return_value = [mock_col1, mock_col2]
        
        # Call the function
        search_tasks_page(self.task_service)
        
        # Verify the header was set
        st.header.assert_called_with("Search Tasks")
        
        # Verify text input was called
        st.text_input.assert_called_with("Search for tasks", placeholder="Enter keyword...")
        
        # Verify write was called with search results
        st.write.assert_any_call("Found 2 tasks matching 'milk':")


if __name__ == "__main__":
    unittest.main()