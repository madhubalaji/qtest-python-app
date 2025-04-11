"""
Custom exceptions for the task manager application.
"""


class TaskManagerException(Exception):
    """Base exception for all task manager exceptions."""
    pass


class TaskNotFoundException(TaskManagerException):
    """Exception raised when a task is not found."""
    pass


class InvalidTaskDataException(TaskManagerException):
    """Exception raised when task data is invalid."""
    pass
