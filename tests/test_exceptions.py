"""
Tests for the custom exceptions module.
"""

import unittest
from src.utils.exceptions import (
    TaskManagerException,
    TaskNotFoundException,
    InvalidTaskDataException
)


class TestExceptions(unittest.TestCase):
    """Test cases for the custom exceptions."""

    def test_task_manager_exception(self):
        """Test the base TaskManagerException."""
        exception = TaskManagerException("Test exception")
        self.assertEqual(str(exception), "Test exception")
        self.assertIsInstance(exception, Exception)

    def test_task_not_found_exception(self):
        """Test the TaskNotFoundException."""
        exception = TaskNotFoundException("Task with ID 1 not found")
        self.assertEqual(str(exception), "Task with ID 1 not found")
        self.assertIsInstance(exception, TaskManagerException)
        self.assertIsInstance(exception, Exception)

    def test_invalid_task_data_exception(self):
        """Test the InvalidTaskDataException."""
        exception = InvalidTaskDataException("Invalid task data: missing title")
        self.assertEqual(str(exception), "Invalid task data: missing title")
        self.assertIsInstance(exception, TaskManagerException)
        self.assertIsInstance(exception, Exception)


if __name__ == "__main__":
    unittest.main()