"""
Tests for the TaskService class.
"""

import os
import pytest
import tempfile
from src.models.task import Task
from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test cases for the TaskService class."""

    def test_task_service_initialization(self, task_service):
        """Test TaskService initialization."""
        assert isinstance(task_service, TaskService)
        assert task_service.tasks == []

    def test_add_task(self, task_service):
        """Test adding a new task."""
        task = task_service.add_task("Test Task", "Test description", "high")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.priority == "high"
        assert task.completed is False
        assert len(task_service.tasks) == 1

    def test_add_task_with_defaults(self, task_service):
        """Test adding a task with default values."""
        task = task_service.add_task("Test Task")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False

    def test_add_multiple_tasks(self, task_service):
        """Test adding multiple tasks."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        
        assert task1.id == 1
        assert task2.id == 2
        assert len(task_service.tasks) == 2

    def test_get_all_tasks(self, task_service):
        """Test getting all tasks."""
        task_service.add_task("Task 1")
        task_service.add_task("Task 2")
        
        tasks = task_service.get_all_tasks()
        assert len(tasks) == 2

    def test_get_all_tasks_show_completed_false(self, task_service):
        """Test getting tasks without completed ones."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task_service.complete_task(task2.id)
        
        tasks = task_service.get_all_tasks(show_completed=False)
        assert len(tasks) == 1
        assert tasks[0].id == task1.id

    def test_get_task_by_id(self, task_service):
        """Test getting a task by ID."""
        task = task_service.add_task("Test Task")
        retrieved_task = task_service.get_task_by_id(task.id)
        
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title

    def test_get_task_by_id_not_found(self, task_service):
        """Test getting a non-existent task by ID."""
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(999)

    def test_update_task(self, task_service):
        """Test updating a task."""
        task = task_service.add_task("Original Title", "Original description", "low")
        
        updated_task = task_service.update_task(
            task.id,
            title="Updated Title",
            description="Updated description",
            priority="high",
            completed=True
        )
        
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated description"
        assert updated_task.priority == "high"
        assert updated_task.completed is True

    def test_update_task_partial(self, task_service):
        """Test updating a task with partial data."""
        task = task_service.add_task("Original Title", "Original description", "low")
        
        updated_task = task_service.update_task(task.id, title="Updated Title")
        
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original description"  # Unchanged
        assert updated_task.priority == "low"  # Unchanged

    def test_update_task_not_found(self, task_service):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service.update_task(999, title="Updated Title")

    def test_complete_task(self, task_service):
        """Test marking a task as complete."""
        task = task_service.add_task("Test Task")
        completed_task = task_service.complete_task(task.id)
        
        assert completed_task.completed is True

    def test_complete_task_not_found(self, task_service):
        """Test completing a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service.complete_task(999)

    def test_delete_task(self, task_service):
        """Test deleting a task."""
        task = task_service.add_task("Test Task")
        assert len(task_service.tasks) == 1
        
        deleted_task = task_service.delete_task(task.id)
        
        assert deleted_task.id == task.id
        assert len(task_service.tasks) == 0

    def test_delete_task_not_found(self, task_service):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service.delete_task(999)

    def test_delete_task_multiple(self, task_service):
        """Test deleting one task from multiple tasks."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task3 = task_service.add_task("Task 3")
        
        assert len(task_service.tasks) == 3
        
        deleted_task = task_service.delete_task(task2.id)
        
        assert deleted_task.id == task2.id
        assert len(task_service.tasks) == 2
        
        remaining_ids = [task.id for task in task_service.tasks]
        assert task1.id in remaining_ids
        assert task3.id in remaining_ids
        assert task2.id not in remaining_ids

    def test_search_tasks(self, task_service):
        """Test searching for tasks."""
        task_service.add_task("Python Programming", "Learn Python basics")
        task_service.add_task("Java Development", "Build Java application")
        task_service.add_task("Database Design", "Design Python database")
        
        results = task_service.search_tasks("Python")
        assert len(results) == 2
        
        titles = [task.title for task in results]
        assert "Python Programming" in titles
        assert "Database Design" in titles

    def test_search_tasks_case_insensitive(self, task_service):
        """Test case-insensitive search."""
        task_service.add_task("Python Programming", "Learn Python basics")
        
        results = task_service.search_tasks("python")
        assert len(results) == 1
        assert results[0].title == "Python Programming"

    def test_search_tasks_in_description(self, task_service):
        """Test searching in task descriptions."""
        task_service.add_task("Task 1", "This contains Python code")
        task_service.add_task("Task 2", "This is about Java")
        
        results = task_service.search_tasks("Python")
        assert len(results) == 1
        assert results[0].title == "Task 1"

    def test_search_tasks_no_results(self, task_service):
        """Test search with no matching results."""
        task_service.add_task("Task 1", "Description 1")
        
        results = task_service.search_tasks("nonexistent")
        assert len(results) == 0

    def test_persistence_save_and_load(self, temp_storage_file):
        """Test saving and loading tasks from file."""
        # Create service and add tasks
        service1 = TaskService(temp_storage_file)
        task1 = service1.add_task("Task 1", "Description 1", "high")
        task2 = service1.add_task("Task 2", "Description 2", "low")
        
        # Create new service instance with same file
        service2 = TaskService(temp_storage_file)
        
        # Should load the saved tasks
        assert len(service2.tasks) == 2
        
        loaded_task1 = service2.get_task_by_id(task1.id)
        loaded_task2 = service2.get_task_by_id(task2.id)
        
        assert loaded_task1.title == "Task 1"
        assert loaded_task1.description == "Description 1"
        assert loaded_task1.priority == "high"
        
        assert loaded_task2.title == "Task 2"
        assert loaded_task2.description == "Description 2"
        assert loaded_task2.priority == "low"

    def test_persistence_delete_and_reload(self, temp_storage_file):
        """Test that deletions are persisted."""
        # Create service and add tasks
        service1 = TaskService(temp_storage_file)
        task1 = service1.add_task("Task 1")
        task2 = service1.add_task("Task 2")
        
        # Delete one task
        service1.delete_task(task1.id)
        
        # Create new service instance with same file
        service2 = TaskService(temp_storage_file)
        
        # Should only have the remaining task
        assert len(service2.tasks) == 1
        assert service2.tasks[0].id == task2.id
        
        # Deleted task should not be found
        with pytest.raises(TaskNotFoundException):
            service2.get_task_by_id(task1.id)