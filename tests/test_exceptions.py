"""Tests for custom exceptions."""

import pytest
from src.utils.exceptions import (
    TaskManagerException,
    TaskNotFoundException,
    InvalidTaskDataException
)


class TestExceptions:
    """Test cases for custom exceptions."""

    def test_task_manager_exception(self):
        """Test base TaskManagerException."""
        with pytest.raises(TaskManagerException):
            raise TaskManagerException("Base exception")

    def test_task_not_found_exception(self):
        """Test TaskNotFoundException."""
        with pytest.raises(TaskNotFoundException):
            raise TaskNotFoundException("Task not found")
        
        # Test inheritance
        with pytest.raises(TaskManagerException):
            raise TaskNotFoundException("Task not found")

    def test_invalid_task_data_exception(self):
        """Test InvalidTaskDataException."""
        with pytest.raises(InvalidTaskDataException):
            raise InvalidTaskDataException("Invalid data")
        
        # Test inheritance
        with pytest.raises(TaskManagerException):
            raise InvalidTaskDataException("Invalid data")

    def test_exception_messages(self):
        """Test that exception messages are preserved."""
        message = "Custom error message"
        
        try:
            raise TaskNotFoundException(message)
        except TaskNotFoundException as e:
            assert str(e) == message

        try:
            raise InvalidTaskDataException(message)
        except InvalidTaskDataException as e:
            assert str(e) == message