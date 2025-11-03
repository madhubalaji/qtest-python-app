"""
Task service for managing task operations.
"""

import os
import json
from typing import List, Dict, Any, Optional

from src.models.task import Task
from src.services.history_service import HistoryService
from src.utils.exceptions import TaskNotFoundException


class TaskService:
    """Service class for managing tasks."""

    def __init__(self, storage_file: str = "tasks.json"):
        """
        Initialize the TaskService with a storage file.

        Args:
            storage_file: Path to the JSON file for storing tasks
        """
        self.storage_file = storage_file
        self.tasks = self._load_tasks()
        
        # INITIALISATION DU SERVICE D'HISTORIQUE AVEC FICHIER SÉPARÉ
        history_dir = os.path.dirname(storage_file) if os.path.dirname(storage_file) else "."
        history_file = os.path.join(history_dir, "task_history.json")
        self.history_service = HistoryService(history_file)

    def _load_tasks(self) -> List[Task]:
        """
        Load tasks from the storage file.

        Returns:
            List of Task objects
        """
        tasks = []
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    task_dicts = json.load(f)
                    tasks = [Task.from_dict(task_dict) for task_dict in task_dicts]
            except json.JSONDecodeError:
                print(f"Error reading task file. Starting with empty task list.")
        return tasks

    def _save_tasks(self) -> None:
        """Save tasks to the storage file."""
        task_dicts = [task.to_dict() for task in self.tasks]
        with open(self.storage_file, "w") as f:
            json.dump(task_dicts, f, indent=2)

    def add_task(self, title: str, description: str = "", severity: str = "medium") -> Task:
        """
        Add a new task.

        Args:
            title: Task title
            description: Task description
            severity: Task severity (low, medium, high)

        Returns:
            The newly created Task
        """
        task_id = max([task.id for task in self.tasks], default=0) + 1
        task = Task(task_id, title, description, severity)
        self.tasks.append(task)
        self._save_tasks()
        
        # ENREGISTREMENT DE L'HISTORIQUE POUR LA CRÉATION DE TÂCHE
        self.history_service.add_history_entry(
            task_id=task.id,
            action_type="create",
            new_values=task.to_dict()
        )
        
        return task

    def get_all_tasks(self, show_completed: bool = True) -> List[Task]:
        """
        Get all tasks, optionally filtering out completed tasks.

        Args:
            show_completed: Whether to include completed tasks

        Returns:
            List of Task objects
        """
        if show_completed:
            return self.tasks
        return [task for task in self.tasks if not task.completed]

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Get a task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            The requested Task

        Raises:
            TaskNotFoundException: If no task with the given ID exists
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundException(f"Task with ID {task_id} not found")

    def update_task(self, task_id: int, **kwargs) -> Task:
        """
        Update a task with the given ID.

        Args:
            task_id: ID of the task to update
            **kwargs: Task attributes to update

        Returns:
            The updated Task

        Raises:
            TaskNotFoundException: If no task with the given ID exists
        """
        task = self.get_task_by_id(task_id)
        
        # SAUVEGARDE DES ANCIENNES VALEURS POUR L'HISTORIQUE
        old_values = task.to_dict()
        
        if "title" in kwargs:
            task.title = kwargs["title"]
        if "description" in kwargs:
            task.description = kwargs["description"]
        if "severity" in kwargs:
            task.severity = kwargs["severity"]
        # COMPATIBILITÉ AVEC L'ANCIEN PARAMÈTRE "PRIORITY"
        if "priority" in kwargs:
            task.severity = kwargs["priority"]
        if "completed" in kwargs:
            task.completed = kwargs["completed"]
            
        self._save_tasks()
        
        # ENREGISTREMENT DE L'HISTORIQUE POUR LA MISE À JOUR
        new_values = task.to_dict()
        self.history_service.add_history_entry(
            task_id=task.id,
            action_type="update",
            old_values=old_values,
            new_values=new_values
        )
        
        return task

    def complete_task(self, task_id: int) -> Task:
        """
        Mark a task as complete.

        Args:
            task_id: ID of the task to mark as complete

        Returns:
            The updated Task

        Raises:
            TaskNotFoundException: If no task with the given ID exists
        """
        task = self.get_task_by_id(task_id)
        
        # SAUVEGARDE DES ANCIENNES VALEURS POUR L'HISTORIQUE
        old_values = task.to_dict()
        
        task.completed = True
        self._save_tasks()
        
        # ENREGISTREMENT DE L'HISTORIQUE POUR LA COMPLÉTION
        new_values = task.to_dict()
        self.history_service.add_history_entry(
            task_id=task.id,
            action_type="complete",
            old_values=old_values,
            new_values=new_values
        )
        
        return task

    def delete_task(self, task_id: int) -> Task:
        """
        Delete a task.

        Args:
            task_id: ID of the task to delete

        Returns:
            The deleted Task

        Raises:
            TaskNotFoundException: If no task with the given ID exists
        """
        task = self.get_task_by_id(task_id)
        self.tasks.remove(task)
        self._save_tasks()
        return task

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search for tasks containing the keyword.

        Args:
            keyword: Keyword to search for in task titles and descriptions

        Returns:
            List of matching Task objects
        """
        keyword = keyword.lower()
        return [
            task for task in self.tasks
            if keyword in task.title.lower() or keyword in task.description.lower()
        ]
