"""
Task history model for tracking task operations and changes.
"""

from datetime import datetime
from typing import Dict, Any, Optional


class TaskHistory:
    """Task history model class representing a single history entry."""

    def __init__(
        self,
        history_id: int,
        task_id: int,
        action_type: str,
        timestamp: Optional[str] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        description: str = ""
    ):
        """
        Initialize a new TaskHistory instance.

        Args:
            history_id: Unique identifier for the history entry
            task_id: ID of the task this history entry relates to
            action_type: Type of action (create, update, complete, delete)
            timestamp: When the action occurred
            old_values: Previous values before the change
            new_values: New values after the change
            description: Human-readable description of the change
        """
        self.id = history_id
        self.task_id = task_id
        self.action_type = action_type
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.old_values = old_values or {}
        self.new_values = new_values or {}
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the history entry to a dictionary representation.

        Returns:
            Dictionary representation of the history entry
        """
        return {
            "id": self.id,
            "task_id": self.task_id,
            "action_type": self.action_type,
            "timestamp": self.timestamp,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskHistory':
        """
        Create a TaskHistory instance from a dictionary.

        Args:
            data: Dictionary containing history data

        Returns:
            A new TaskHistory instance
        """
        return cls(
            history_id=data["id"],
            task_id=data["task_id"],
            action_type=data["action_type"],
            timestamp=data.get("timestamp"),
            old_values=data.get("old_values", {}),
            new_values=data.get("new_values", {}),
            description=data.get("description", "")
        )

    def __str__(self) -> str:
        """String representation of the history entry."""
        return f"History {self.id}: Task {self.task_id} - {self.action_type} at {self.timestamp}"