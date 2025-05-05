"""
Task model representing a task entity in the task manager application.
"""

from datetime import datetime
from typing import Dict, Any, Optional


class Task:
    """Task model class representing a single task."""

    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        priority: str = "medium",
        completed: bool = False,
        created_at: Optional[str] = None,
        assigned_to: str = "unassigned"
    ):
        """
        Initialize a new Task instance.

        Args:
            task_id: Unique identifier for the task
            title: Title of the task
            description: Detailed description of the task
            priority: Priority level (low, medium, high)
            completed: Whether the task is completed
            created_at: Timestamp when the task was created
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assigned_to = assigned_to

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the task to a dictionary representation.

        Returns:
            Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at,
            "assigned_to": self.assigned_to
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Create a Task instance from a dictionary.

        Args:
            data: Dictionary containing task data

        Returns:
            A new Task instance
        """
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            assigned_to=data.get("assigned_to", "unassigned")
        )

    def __str__(self) -> str:
        """String representation of the task."""
        status = "Completed" if self.completed else "Active"
        return f"Task {self.id}: {self.title} ({status}, {self.priority} priority)"
