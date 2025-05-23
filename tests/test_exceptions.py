"""
Tests for the custom exceptions.
"""

import unittest
from src.utils.exceptions import TaskManagerException, TaskNotFoundException, InvalidTaskDataException


class TestExceptions(unittest.TestCase):
    """Test cases for the custom exceptions."""

    def test_task_manager_exception(self):
        """Test the TaskManagerException."""
        # Create an exception
        exception = TaskManagerException("General error")
        
        # Check the exception message
        self.assertEqual(str(exception), "General error")
        
        # Check that it's an instance of Exception
        self.assertIsInstance(exception, Exception)

    def test_task_not_found_exception(self):
        """Test the TaskNotFoundException."""
        # Create an exception
        exception = TaskNotFoundException("Task with ID 1 not found")
        
        # Check the exception message
        self.assertEqual(str(exception), "Task with ID 1 not found")
        
        # Check that it's an instance of TaskManagerException
        self.assertIsInstance(exception, TaskManagerException)

    def test_invalid_task_data_exception(self):
        """Test the InvalidTaskDataException."""
        # Create an exception
        exception = InvalidTaskDataException("Invalid task data: missing title")
        
        # Check the exception message
        self.assertEqual(str(exception), "Invalid task data: missing title")
        
        # Check that it's an instance of TaskManagerException
        self.assertIsInstance(exception, TaskManagerException)

    def test_exception_hierarchy(self):
        """Test the exception hierarchy."""
        # Create exceptions
        task_manager_exception = TaskManagerException("General error")
        task_not_found_exception = TaskNotFoundException("Task not found")
        invalid_task_data_exception = InvalidTaskDataException("Invalid data")
        
        # Check the hierarchy
        self.assertIsInstance(task_manager_exception, Exception)
        self.assertIsInstance(task_not_found_exception, TaskManagerException)
        self.assertIsInstance(invalid_task_data_exception, TaskManagerException)


if __name__ == "__main__":
    unittest.main()