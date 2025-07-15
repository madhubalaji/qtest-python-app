"""
Tests for the TaskService class.
"""

import unittest
import os
import json
import tempfile
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService(unittest.TestCase):
    """Test cases for the TaskService class."""

    def setUp(self):
        """Set up a temporary file for task storage."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.task_service = TaskService(self.temp_file.name)

    def tearDown(self):
        """Clean up the temporary file."""
        os.unlink(self.temp_file.name)

    def test_add_task(self):
        """Test adding a task."""
        task = self.task_service.add_task("Test Task", "This is a test task", "high")
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.priority, "high")
        self.assertFalse(task.completed)

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks."""
        task1 = self.task_service.add_task("Task 1")
        task2 = self.task_service.add_task("Task 2")
        task3 = self.task_service.add_task("Task 3")
        
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        self.task_service.add_task("Task 1")
        self.task_service.add_task("Task 2")
        self.task_service.add_task("Task 3")
        
        tasks = self.task_service.get_all_tasks()
        
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")
        self.assertEqual(tasks[2].title, "Task 3")

    def test_get_all_tasks_filter_completed(self):
        """Test getting all tasks with completed filter."""
        task1 = self.task_service.add_task("Task 1")
        task2 = self.task_service.add_task("Task 2")
        task3 = self.task_service.add_task("Task 3")
        
        self.task_service.complete_task(task1.id)
        self.task_service.complete_task(task3.id)
        
        # Get all tasks including completed
        all_tasks = self.task_service.get_all_tasks(show_completed=True)
        self.assertEqual(len(all_tasks), 3)
        
        # Get only active tasks
        active_tasks = self.task_service.get_all_tasks(show_completed=False)
        self.assertEqual(len(active_tasks), 1)
        self.assertEqual(active_tasks[0].id, task2.id)

    def test_get_task_by_id(self):
        """Test getting a task by ID."""
        task = self.task_service.add_task("Test Task")
        
        retrieved_task = self.task_service.get_task_by_id(task.id)
        
        self.assertEqual(retrieved_task.id, task.id)
        self.assertEqual(retrieved_task.title, task.title)

    def test_get_task_by_id_not_found(self):
        """Test getting a task by ID that doesn't exist."""
        with self.assertRaises(TaskNotFoundException):
            self.task_service.get_task_by_id(999)

    def test_update_task(self):
        """Test updating a task."""
        task = self.task_service.add_task("Test Task", "Original description", "low")
        
        updated_task = self.task_service.update_task(
            task.id,
            title="Updated Task",
            description="Updated description",
            priority="high"
        )
        
        self.assertEqual(updated_task.id, task.id)
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.description, "Updated description")
        self.assertEqual(updated_task.priority, "high")
        
        # Verify the task was actually updated in storage
        retrieved_task = self.task_service.get_task_by_id(task.id)
        self.assertEqual(retrieved_task.title, "Updated Task")
        self.assertEqual(retrieved_task.description, "Updated description")
        self.assertEqual(retrieved_task.priority, "high")

    def test_update_task_partial(self):
        """Test partially updating a task."""
        task = self.task_service.add_task("Test Task", "Original description", "low")
        
        # Only update the title
        updated_task = self.task_service.update_task(task.id, title="Updated Task")
        
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.description, "Original description")
        self.assertEqual(updated_task.priority, "low")

    def test_update_task_not_found(self):
        """Test updating a task that doesn't exist."""
        with self.assertRaises(TaskNotFoundException):
            self.task_service.update_task(999, title="Updated Task")

    def test_complete_task(self):
        """Test marking a task as complete."""
        task = self.task_service.add_task("Test Task")
        self.assertFalse(task.completed)
        
        completed_task = self.task_service.complete_task(task.id)
        self.assertTrue(completed_task.completed)
        
        # Verify the task was actually updated in storage
        retrieved_task = self.task_service.get_task_by_id(task.id)
        self.assertTrue(retrieved_task.completed)

    def test_complete_task_not_found(self):
        """Test completing a task that doesn't exist."""
        with self.assertRaises(TaskNotFoundException):
            self.task_service.complete_task(999)

    def test_delete_task(self):
        """Test deleting a task."""
        task = self.task_service.add_task("Test Task")
        
        deleted_task = self.task_service.delete_task(task.id)
        self.assertEqual(deleted_task.id, task.id)
        
        # Verify the task was actually deleted
        with self.assertRaises(TaskNotFoundException):
            self.task_service.get_task_by_id(task.id)

    def test_delete_task_not_found(self):
        """Test deleting a task that doesn't exist."""
        with self.assertRaises(TaskNotFoundException):
            self.task_service.delete_task(999)

    def test_search_tasks(self):
        """Test searching for tasks."""
        self.task_service.add_task("Buy groceries", "Get milk and eggs")
        self.task_service.add_task("Clean house", "Vacuum and dust")
        self.task_service.add_task("Pay bills", "Electricity and water")
        self.task_service.add_task("Buy milk", "Get whole milk")
        
        # Search in title
        results = self.task_service.search_tasks("buy")
        self.assertEqual(len(results), 2)
        
        # Search in description
        results = self.task_service.search_tasks("milk")
        self.assertEqual(len(results), 2)
        
        # Search with no results
        results = self.task_service.search_tasks("nonexistent")
        self.assertEqual(len(results), 0)

    def test_load_tasks_from_file(self):
        """Test loading tasks from a file."""
        # Create a file with some tasks
        tasks_data = [
            {
                "id": 1,
                "title": "Task 1",
                "description": "Description 1",
                "priority": "low",
                "completed": False,
                "created_at": "2023-01-01 12:00:00"
            },
            {
                "id": 2,
                "title": "Task 2",
                "description": "Description 2",
                "priority": "high",
                "completed": True,
                "created_at": "2023-01-02 12:00:00"
            }
        ]
        
        with open(self.temp_file.name, "w") as f:
            json.dump(tasks_data, f)
        
        # Create a new TaskService that will load from the file
        task_service = TaskService(self.temp_file.name)
        
        tasks = task_service.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[1].title, "Task 2")
        self.assertTrue(tasks[1].completed)

    def test_save_tasks_to_file(self):
        """Test saving tasks to a file."""
        self.task_service.add_task("Task 1", "Description 1", "low")
        self.task_service.add_task("Task 2", "Description 2", "high")
        
        # Create a new TaskService that will load from the same file
        new_task_service = TaskService(self.temp_file.name)
        
        tasks = new_task_service.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")


if __name__ == "__main__":
    unittest.main()