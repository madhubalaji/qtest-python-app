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
        severity: str = "medium",
        completed: bool = False,
        created_at: Optional[str] = None,
        # COMPATIBILITÉ AVEC LES ANCIENNES DONNÉES UTILISANT "PRIORITY"
        priority: Optional[str] = None
    ):
        """
        Initialize a new Task instance.

        Args:
            task_id: Unique identifier for the task
            title: Title of the task
            description: Detailed description of the task
            severity: Severity level (low, medium, high)
            completed: Whether the task is completed
            created_at: Timestamp when the task was created
            priority: Legacy parameter for backward compatibility
        """
        self.id = task_id
        self.title = title
        self.description = description
        # MIGRATION AUTOMATIQUE DE "PRIORITY" VERS "SEVERITY" POUR COMPATIBILITÉ
        self.severity = priority if priority is not None else severity
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            "severity": self.severity,
            "completed": self.completed,
            "created_at": self.created_at
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
        # SUPPORT POUR LES ANCIENNES DONNÉES AVEC "PRIORITY" ET NOUVELLES AVEC "SEVERITY"
        severity = data.get("severity")
        priority = data.get("priority")
        
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            severity=severity if severity is not None else "medium",
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            priority=priority
        )

    def __str__(self) -> str:
        """String representation of the task."""
        status = "Completed" if self.completed else "Active"
        return f"Task {self.id}: {self.title} ({status}, {self.severity} severity)"
