"""
Integration tests for the task manager application.
"""

import os
import tempfile
import pytest
from src.models.task import Task
from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


class TestIntegration:
    """Integration test cases."""

    def test_full_task_lifecycle(self, task_service):
        """Test complete task lifecycle: create, read, update, delete."""
        # Create task
        task = task_service.add_task("Integration Test Task", "Test description", "high")
        assert task.id == 1
        assert len(task_service.tasks) == 1

        # Read task
        retrieved_task = task_service.get_task_by_id(task.id)
        assert retrieved_task.title == "Integration Test Task"
        assert retrieved_task.description == "Test description"
        assert retrieved_task.priority == "high"
        assert retrieved_task.completed is False

        # Update task
        updated_task = task_service.update_task(
            task.id,
            title="Updated Task",
            description="Updated description",
            priority="low"
        )
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated description"
        assert updated_task.priority == "low"

        # Complete task
        completed_task = task_service.complete_task(task.id)
        assert completed_task.completed is True

        # Delete task
        deleted_task = task_service.delete_task(task.id)
        assert deleted_task.id == task.id
        assert len(task_service.tasks) == 0

        # Verify task is gone
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(task.id)

    def test_multiple_tasks_operations(self, task_service):
        """Test operations with multiple tasks."""
        # Add multiple tasks
        task1 = task_service.add_task("Task 1", "Description 1", "high")
        task2 = task_service.add_task("Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Task 3", "Description 3", "low")

        assert len(task_service.tasks) == 3

        # Complete one task
        task_service.complete_task(task2.id)

        # Get all tasks (including completed)
        all_tasks = task_service.get_all_tasks(show_completed=True)
        assert len(all_tasks) == 3

        # Get only active tasks
        active_tasks = task_service.get_all_tasks(show_completed=False)
        assert len(active_tasks) == 2
        active_ids = [task.id for task in active_tasks]
        assert task1.id in active_ids
        assert task3.id in active_ids
        assert task2.id not in active_ids

        # Delete one task
        task_service.delete_task(task1.id)
        assert len(task_service.tasks) == 2

        # Search for remaining tasks
        results = task_service.search_tasks("Task")
        assert len(results) == 2

    def test_search_and_delete_workflow(self, task_service):
        """Test searching for tasks and then deleting them."""
        # Add tasks with different content
        task1 = task_service.add_task("Python Project", "Build a Python application")
        task2 = task_service.add_task("Java Project", "Build a Java application")
        task3 = task_service.add_task("Python Tutorial", "Learn Python basics")

        # Search for Python-related tasks
        python_tasks = task_service.search_tasks("Python")
        assert len(python_tasks) == 2

        # Delete Python tasks
        for task in python_tasks:
            task_service.delete_task(task.id)

        # Verify only Java task remains
        remaining_tasks = task_service.get_all_tasks()
        assert len(remaining_tasks) == 1
        assert remaining_tasks[0].title == "Java Project"

    def test_task_persistence_with_operations(self, temp_storage_file):
        """Test that all operations are properly persisted."""
        # Create first service instance
        service1 = TaskService(temp_storage_file)
        
        # Add tasks
        task1 = service1.add_task("Persistent Task 1", "Description 1", "high")
        task2 = service1.add_task("Persistent Task 2", "Description 2", "medium")
        task3 = service1.add_task("Persistent Task 3", "Description 3", "low")

        # Perform operations
        service1.complete_task(task2.id)
        service1.update_task(task1.id, title="Updated Persistent Task 1")
        service1.delete_task(task3.id)

        # Create second service instance (simulating app restart)
        service2 = TaskService(temp_storage_file)

        # Verify persistence
        assert len(service2.tasks) == 2

        # Check task1 (updated)
        loaded_task1 = service2.get_task_by_id(task1.id)
        assert loaded_task1.title == "Updated Persistent Task 1"
        assert loaded_task1.description == "Description 1"
        assert loaded_task1.priority == "high"
        assert loaded_task1.completed is False

        # Check task2 (completed)
        loaded_task2 = service2.get_task_by_id(task2.id)
        assert loaded_task2.title == "Persistent Task 2"
        assert loaded_task2.completed is True

        # Check task3 (deleted)
        with pytest.raises(TaskNotFoundException):
            service2.get_task_by_id(task3.id)

    def test_edge_cases_and_error_handling(self, task_service):
        """Test edge cases and error handling."""
        # Test operations on empty service
        assert len(task_service.get_all_tasks()) == 0
        assert len(task_service.search_tasks("anything")) == 0

        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(1)

        with pytest.raises(TaskNotFoundException):
            task_service.update_task(1, title="New Title")

        with pytest.raises(TaskNotFoundException):
            task_service.complete_task(1)

        with pytest.raises(TaskNotFoundException):
            task_service.delete_task(1)

        # Add a task and test operations
        task = task_service.add_task("Test Task")

        # Test double completion
        task_service.complete_task(task.id)
        completed_again = task_service.complete_task(task.id)
        assert completed_again.completed is True

        # Test deletion of completed task
        deleted_task = task_service.delete_task(task.id)
        assert deleted_task.completed is True

    def test_task_id_generation(self, task_service):
        """Test that task IDs are generated correctly."""
        # Add tasks
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task3 = task_service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

        # Delete middle task
        task_service.delete_task(task2.id)

        # Add new task - should get next available ID
        task4 = task_service.add_task("Task 4")
        assert task4.id == 4  # Should be 4, not 2

    def test_search_functionality_comprehensive(self, task_service):
        """Test comprehensive search functionality."""
        # Add diverse tasks
        task_service.add_task("Python Web Development", "Build web apps with Django")
        task_service.add_task("Machine Learning", "Learn Python for ML")
        task_service.add_task("Database Administration", "Manage PostgreSQL databases")
        task_service.add_task("Frontend Development", "Build React applications")

        # Test various search terms
        python_results = task_service.search_tasks("Python")
        assert len(python_results) == 2

        web_results = task_service.search_tasks("web")
        assert len(web_results) == 1

        development_results = task_service.search_tasks("Development")
        assert len(development_results) == 2

        # Test search in descriptions
        django_results = task_service.search_tasks("Django")
        assert len(django_results) == 1

        # Test case insensitive
        PYTHON_results = task_service.search_tasks("PYTHON")
        assert len(PYTHON_results) == 2

        # Test partial matches
        dev_results = task_service.search_tasks("dev")
        assert len(dev_results) == 2