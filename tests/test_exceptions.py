"""
Tests for custom exceptions.
"""

import pytest
from src.utils.exceptions import (
    TaskManagerException,
    TaskNotFoundException,
    InvalidTaskDataException
)


class TestExceptions:
    """Test cases for custom exceptions."""

    def test_task_manager_exception_inheritance(self):
        """Test that TaskManagerException inherits from Exception."""
        exception = TaskManagerException("Test message")
        assert isinstance(exception, Exception)
        assert str(exception) == "Test message"

    def test_task_not_found_exception_inheritance(self):
        """Test that TaskNotFoundException inherits from TaskManagerException."""
        exception = TaskNotFoundException("Task not found")
        assert isinstance(exception, TaskManagerException)
        assert isinstance(exception, Exception)
        assert str(exception) == "Task not found"

    def test_invalid_task_data_exception_inheritance(self):
        """Test that InvalidTaskDataException inherits from TaskManagerException."""
        exception = InvalidTaskDataException("Invalid data")
        assert isinstance(exception, TaskManagerException)
        assert isinstance(exception, Exception)
        assert str(exception) == "Invalid data"

    def test_task_not_found_exception_can_be_raised(self):
        """Test that TaskNotFoundException can be raised and caught."""
        with pytest.raises(TaskNotFoundException) as exc_info:
            raise TaskNotFoundException("Task with ID 1 not found")
        
        assert str(exc_info.value) == "Task with ID 1 not found"

    def test_invalid_task_data_exception_can_be_raised(self):
        """Test that InvalidTaskDataException can be raised and caught."""
        with pytest.raises(InvalidTaskDataException) as exc_info:
            raise InvalidTaskDataException("Title cannot be empty")
        
        assert str(exc_info.value) == "Title cannot be empty"

    def test_exceptions_can_be_caught_as_base_exception(self):
        """Test that specific exceptions can be caught as base TaskManagerException."""
        with pytest.raises(TaskManagerException):
            raise TaskNotFoundException("Test")
        
        with pytest.raises(TaskManagerException):
            raise InvalidTaskDataException("Test")

    def test_exception_without_message(self):
        """Test exceptions without custom messages."""
        exception1 = TaskNotFoundException()
        exception2 = InvalidTaskDataException()
        exception3 = TaskManagerException()
        
        # Should not raise any errors
        assert isinstance(exception1, TaskNotFoundException)
        assert isinstance(exception2, InvalidTaskDataException)
        assert isinstance(exception3, TaskManagerException)