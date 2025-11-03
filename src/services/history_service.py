"""
History service for managing task history operations.
"""

import os
import json
from typing import List, Dict, Any, Optional

from src.models.task_history import TaskHistory


class HistoryService:
    """Service class for managing task history."""

    def __init__(self, storage_file: str = "task_history.json"):
        """
        Initialize the HistoryService with a storage file.

        Args:
            storage_file: Path to the JSON file for storing history
        """
        self.storage_file = storage_file
        self.history_entries = self._load_history()

    def _load_history(self) -> List[TaskHistory]:
        """
        Load history entries from the storage file.

        Returns:
            List of TaskHistory objects
        """
        history_entries = []
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    history_dicts = json.load(f)
                    history_entries = [TaskHistory.from_dict(entry) for entry in history_dicts]
            except json.JSONDecodeError:
                print(f"Error reading history file. Starting with empty history.")
        return history_entries

    def _save_history(self) -> None:
        """Save history entries to the storage file."""
        history_dicts = [entry.to_dict() for entry in self.history_entries]
        with open(self.storage_file, "w") as f:
            json.dump(history_dicts, f, indent=2)

    def add_history_entry(
        self,
        task_id: int,
        action_type: str,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        description: str = ""
    ) -> TaskHistory:
        """
        Add a new history entry.

        Args:
            task_id: ID of the task
            action_type: Type of action (create, update, complete, delete)
            old_values: Previous values before the change
            new_values: New values after the change
            description: Human-readable description of the change

        Returns:
            The newly created TaskHistory entry
        """
        history_id = max([entry.id for entry in self.history_entries], default=0) + 1
        
        # GÉNÉRATION AUTOMATIQUE DE DESCRIPTION SI NON FOURNIE
        if not description:
            description = self._generate_description(action_type, old_values, new_values)
        
        history_entry = TaskHistory(
            history_id=history_id,
            task_id=task_id,
            action_type=action_type,
            old_values=old_values,
            new_values=new_values,
            description=description
        )
        
        self.history_entries.append(history_entry)
        self._save_history()
        return history_entry

    def _generate_description(
        self,
        action_type: str,
        old_values: Optional[Dict[str, Any]],
        new_values: Optional[Dict[str, Any]]
    ) -> str:
        """
        Generate a human-readable description for the history entry.

        Args:
            action_type: Type of action
            old_values: Previous values
            new_values: New values

        Returns:
            Generated description
        """
        if action_type == "create":
            title = new_values.get("title", "Unknown") if new_values else "Unknown"
            return f"Task '{title}' created"
        elif action_type == "update":
            changes = []
            if old_values and new_values:
                for key, new_val in new_values.items():
                    old_val = old_values.get(key)
                    if old_val != new_val:
                        changes.append(f"{key}: '{old_val}' → '{new_val}'")
            return f"Task updated: {', '.join(changes)}" if changes else "Task updated"
        elif action_type == "complete":
            return "Task marked as completed"
        elif action_type == "delete":
            title = old_values.get("title", "Unknown") if old_values else "Unknown"
            return f"Task '{title}' deleted"
        else:
            return f"Task {action_type}"

    def get_task_history(self, task_id: int) -> List[TaskHistory]:
        """
        Get all history entries for a specific task.

        Args:
            task_id: ID of the task

        Returns:
            List of TaskHistory entries for the task
        """
        return [entry for entry in self.history_entries if entry.task_id == task_id]

    def get_all_history(self, limit: Optional[int] = None) -> List[TaskHistory]:
        """
        Get all history entries, optionally limited.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of TaskHistory entries, sorted by timestamp (newest first)
        """
        # TRIER PAR TIMESTAMP DÉCROISSANT (PLUS RÉCENT EN PREMIER)
        sorted_history = sorted(
            self.history_entries,
            key=lambda x: x.timestamp,
            reverse=True
        )
        
        if limit:
            return sorted_history[:limit]
        return sorted_history

    def get_history_by_action(self, action_type: str) -> List[TaskHistory]:
        """
        Get all history entries for a specific action type.

        Args:
            action_type: Type of action to filter by

        Returns:
            List of TaskHistory entries for the action type
        """
        return [entry for entry in self.history_entries if entry.action_type == action_type]

    def clear_task_history(self, task_id: int) -> int:
        """
        Clear all history entries for a specific task.

        Args:
            task_id: ID of the task

        Returns:
            Number of entries removed
        """
        original_count = len(self.history_entries)
        self.history_entries = [entry for entry in self.history_entries if entry.task_id != task_id]
        removed_count = original_count - len(self.history_entries)
        
        if removed_count > 0:
            self._save_history()
        
        return removed_count