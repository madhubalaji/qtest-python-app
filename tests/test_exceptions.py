"""
Unit tests for custom exceptions.
"""

import pytest
from src.utils.exceptions import (
    TaskManagerException,
    TaskNotFoundException,
    InvalidTaskDataException
)


class TestTaskManagerExceptions:
    """Test cases for custom exceptions."""

    def test_task_manager_exception_base(self):
        """Test base TaskManagerException."""
        message = "Base exception message"
        exception = TaskManagerException(message)
        
        assert str(exception) == message
        assert isinstance(exception, Exception)

    def test_task_not_found_exception(self):
        """Test TaskNotFoundException."""
        message = "Task with ID 123 not found"
        exception = TaskNotFoundException(message)
        
        assert str(exception) == message
        assert isinstance(exception, TaskManagerException)
        assert isinstance(exception, Exception)

    def test_invalid_task_data_exception(self):
        """Test InvalidTaskDataException."""
        message = "Invalid task data provided"
        exception = InvalidTaskDataException(message)
        
        assert str(exception) == message
        assert isinstance(exception, TaskManagerException)
        assert isinstance(exception, Exception)

    def test_exception_inheritance_hierarchy(self):
        """Test that exceptions follow proper inheritance hierarchy."""
        # TaskNotFoundException should inherit from TaskManagerException
        assert issubclass(TaskNotFoundException, TaskManagerException)
        
        # InvalidTaskDataException should inherit from TaskManagerException
        assert issubclass(InvalidTaskDataException, TaskManagerException)
        
        # TaskManagerException should inherit from Exception
        assert issubclass(TaskManagerException, Exception)

    def test_raising_task_not_found_exception(self):
        """Test raising TaskNotFoundException."""
        with pytest.raises(TaskNotFoundException) as exc_info:
            raise TaskNotFoundException("Task not found")
        
        assert "Task not found" in str(exc_info.value)

    def test_raising_invalid_task_data_exception(self):
        """Test raising InvalidTaskDataException."""
        with pytest.raises(InvalidTaskDataException) as exc_info:
            raise InvalidTaskDataException("Invalid data")
        
        assert "Invalid data" in str(exc_info.value)

    def test_catching_specific_exception(self):
        """Test catching specific exception types."""
        def raise_task_not_found():
            raise TaskNotFoundException("Specific task not found")
        
        def raise_invalid_data():
            raise InvalidTaskDataException("Specific invalid data")
        
        # Test catching TaskNotFoundException specifically
        with pytest.raises(TaskNotFoundException):
            raise_task_not_found()
        
        # Test catching InvalidTaskDataException specifically
        with pytest.raises(InvalidTaskDataException):
            raise_invalid_data()

    def test_catching_base_exception(self):
        """Test catching base TaskManagerException."""
        def raise_specific_exception():
            raise TaskNotFoundException("Task not found")
        
        # Should be able to catch specific exception with base class
        with pytest.raises(TaskManagerException):
            raise_specific_exception()

    def test_exception_without_message(self):
        """Test exceptions without custom messages."""
        exception = TaskNotFoundException()
        assert isinstance(exception, TaskNotFoundException)
        
        exception = InvalidTaskDataException()
        assert isinstance(exception, InvalidTaskDataException)

    def test_exception_with_empty_message(self):
        """Test exceptions with empty messages."""
        exception = TaskNotFoundException("")
        assert str(exception) == ""
        
        exception = InvalidTaskDataException("")
        assert str(exception) == ""

    def test_exception_with_complex_message(self):
        """Test exceptions with complex messages."""
        complex_message = "Task with ID 42 not found in database. Available IDs: [1, 2, 3]"
        exception = TaskNotFoundException(complex_message)
        assert str(exception) == complex_message