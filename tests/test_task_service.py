"""
Tests for the TaskService class.
"""

import os
import json
import pytest
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException


class TestTaskService:
    """Test cases for the TaskService class."""

    def test_task_service_initialization_new_file(self, temp_storage_file):
        """Test TaskService initialization with a new file."""
        service = TaskService(temp_storage_file)
        
        assert service.storage_file == temp_storage_file
        assert service.tasks == []

    def test_task_service_initialization_existing_file(self, temp_storage_file):
        """Test TaskService initialization with existing file."""
        # Create a file with sample data
        sample_data = [
            {
                "id": 1,
                "title": "Test Task",
                "description": "Test Description",
                "priority": "medium",
                "completed": False,
                "created_at": "2023-01-01 12:00:00"
            }
        ]
        
        with open(temp_storage_file, 'w') as f:
            json.dump(sample_data, f)
        
        service = TaskService(temp_storage_file)
        
        assert len(service.tasks) == 1
        assert service.tasks[0].id == 1
        assert service.tasks[0].title == "Test Task"

    def test_task_service_initialization_corrupted_file(self, temp_storage_file):
        """Test TaskService initialization with corrupted JSON file."""
        # Create a corrupted JSON file
        with open(temp_storage_file, 'w') as f:
            f.write("invalid json content")
        
        service = TaskService(temp_storage_file)
        
        # Should start with empty task list
        assert service.tasks == []

    def test_add_task_basic(self, task_service):
        """Test adding a basic task."""
        task = task_service.add_task("Test Task", "Test Description", "high")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.completed is False
        assert len(task_service.tasks) == 1

    def test_add_task_minimal(self, task_service):
        """Test adding a task with minimal parameters."""
        task = task_service.add_task("Minimal Task")
        
        assert task.id == 1
        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.priority == "medium"
        assert task.completed is False

    def test_add_multiple_tasks_incremental_ids(self, task_service):
        """Test that multiple tasks get incremental IDs."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task3 = task_service.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert len(task_service.tasks) == 3

    def test_add_task_persistence(self, task_service):
        """Test that added tasks are persisted to file."""
        task_service.add_task("Persistent Task")
        
        # Create new service instance with same file
        new_service = TaskService(task_service.storage_file)
        
        assert len(new_service.tasks) == 1
        assert new_service.tasks[0].title == "Persistent Task"

    def test_get_all_tasks_empty(self, task_service):
        """Test getting all tasks when none exist."""
        tasks = task_service.get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_with_completed(self, task_service):
        """Test getting all tasks including completed ones."""
        task1 = task_service.add_task("Active Task")
        task2 = task_service.add_task("Completed Task")
        task_service.complete_task(task2.id)
        
        all_tasks = task_service.get_all_tasks(show_completed=True)
        active_tasks = task_service.get_all_tasks(show_completed=False)
        
        assert len(all_tasks) == 2
        assert len(active_tasks) == 1
        assert active_tasks[0].title == "Active Task"

    def test_get_task_by_id_existing(self, task_service):
        """Test getting an existing task by ID."""
        added_task = task_service.add_task("Test Task")
        retrieved_task = task_service.get_task_by_id(added_task.id)
        
        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title

    def test_get_task_by_id_nonexistent(self, task_service):
        """Test getting a non-existent task by ID."""
        with pytest.raises(TaskNotFoundException) as exc_info:
            task_service.get_task_by_id(999)
        
        assert "Task with ID 999 not found" in str(exc_info.value)

    def test_update_task_title(self, task_service):
        """Test updating task title."""
        task = task_service.add_task("Original Title")
        updated_task = task_service.update_task(task.id, title="Updated Title")
        
        assert updated_task.title == "Updated Title"
        assert updated_task.id == task.id

    def test_update_task_description(self, task_service):
        """Test updating task description."""
        task = task_service.add_task("Test Task", "Original Description")
        updated_task = task_service.update_task(task.id, description="Updated Description")
        
        assert updated_task.description == "Updated Description"

    def test_update_task_priority(self, task_service):
        """Test updating task priority."""
        task = task_service.add_task("Test Task", priority="low")
        updated_task = task_service.update_task(task.id, priority="high")
        
        assert updated_task.priority == "high"

    def test_update_task_completed(self, task_service):
        """Test updating task completion status."""
        task = task_service.add_task("Test Task")
        updated_task = task_service.update_task(task.id, completed=True)
        
        assert updated_task.completed is True

    def test_update_task_multiple_fields(self, task_service):
        """Test updating multiple task fields at once."""
        task = task_service.add_task("Test Task")
        updated_task = task_service.update_task(
            task.id,
            title="Updated Title",
            description="Updated Description",
            priority="high",
            completed=True
        )
        
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == "high"
        assert updated_task.completed is True

    def test_update_task_nonexistent(self, task_service):
        """Test updating a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service.update_task(999, title="Updated Title")

    def test_update_task_persistence(self, task_service):
        """Test that task updates are persisted."""
        task = task_service.add_task("Test Task")
        task_service.update_task(task.id, title="Updated Title")
        
        # Create new service instance
        new_service = TaskService(task_service.storage_file)
        retrieved_task = new_service.get_task_by_id(task.id)
        
        assert retrieved_task.title == "Updated Title"

    def test_complete_task(self, task_service):
        """Test marking a task as complete."""
        task = task_service.add_task("Test Task")
        completed_task = task_service.complete_task(task.id)
        
        assert completed_task.completed is True
        assert completed_task.id == task.id

    def test_complete_task_nonexistent(self, task_service):
        """Test completing a non-existent task."""
        with pytest.raises(TaskNotFoundException):
            task_service.complete_task(999)

    def test_delete_task_existing(self, task_service):
        """Test deleting an existing task."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task3 = task_service.add_task("Task 3")
        
        deleted_task = task_service.delete_task(task2.id)
        
        assert deleted_task.id == task2.id
        assert deleted_task.title == "Task 2"
        assert len(task_service.tasks) == 2
        
        # Verify the correct task was deleted
        remaining_tasks = task_service.get_all_tasks()
        remaining_ids = [task.id for task in remaining_tasks]
        assert task1.id in remaining_ids
        assert task2.id not in remaining_ids
        assert task3.id in remaining_ids

    def test_delete_task_nonexistent(self, task_service):
        """Test deleting a non-existent task."""
        with pytest.raises(TaskNotFoundException) as exc_info:
            task_service.delete_task(999)
        
        assert "Task with ID 999 not found" in str(exc_info.value)

    def test_delete_task_persistence(self, task_service):
        """Test that task deletion is persisted."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        
        task_service.delete_task(task1.id)
        
        # Create new service instance
        new_service = TaskService(task_service.storage_file)
        
        assert len(new_service.tasks) == 1
        assert new_service.tasks[0].id == task2.id

    def test_delete_all_tasks(self, task_service):
        """Test deleting all tasks."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        
        task_service.delete_task(task1.id)
        task_service.delete_task(task2.id)
        
        assert len(task_service.tasks) == 0

    def test_search_tasks_empty(self, task_service):
        """Test searching when no tasks exist."""
        results = task_service.search_tasks("test")
        assert results == []

    def test_search_tasks_no_matches(self, task_service):
        """Test searching with no matches."""
        task_service.add_task("Task 1", "Description 1")
        results = task_service.search_tasks("nonexistent")
        assert results == []

    def test_search_tasks_title_match(self, task_service):
        """Test searching by title."""
        task1 = task_service.add_task("Important Task", "Description")
        task2 = task_service.add_task("Regular Task", "Description")
        
        results = task_service.search_tasks("Important")
        
        assert len(results) == 1
        assert results[0].id == task1.id

    def test_search_tasks_description_match(self, task_service):
        """Test searching by description."""
        task1 = task_service.add_task("Task 1", "Important work")
        task2 = task_service.add_task("Task 2", "Regular work")
        
        results = task_service.search_tasks("Important")
        
        assert len(results) == 1
        assert results[0].id == task1.id

    def test_search_tasks_case_insensitive(self, task_service):
        """Test that search is case insensitive."""
        task = task_service.add_task("Important Task", "Description")
        
        results_lower = task_service.search_tasks("important")
        results_upper = task_service.search_tasks("IMPORTANT")
        results_mixed = task_service.search_tasks("ImPoRtAnT")
        
        assert len(results_lower) == 1
        assert len(results_upper) == 1
        assert len(results_mixed) == 1
        assert results_lower[0].id == task.id
        assert results_upper[0].id == task.id
        assert results_mixed[0].id == task.id

    def test_search_tasks_multiple_matches(self, task_service):
        """Test searching with multiple matches."""
        task1 = task_service.add_task("Work Task", "Important work")
        task2 = task_service.add_task("Personal Task", "Work on hobby")
        task3 = task_service.add_task("Shopping", "Buy groceries")
        
        results = task_service.search_tasks("work")
        
        assert len(results) == 2
        result_ids = [task.id for task in results]
        assert task1.id in result_ids
        assert task2.id in result_ids
        assert task3.id not in result_ids

    def test_search_tasks_partial_match(self, task_service):
        """Test searching with partial keyword matches."""
        task = task_service.add_task("Programming", "Write Python code")
        
        results = task_service.search_tasks("prog")
        
        assert len(results) == 1
        assert results[0].id == task.id

    def test_task_service_workflow_integration(self, task_service):
        """Test a complete workflow with multiple operations."""
        # Add tasks
        task1 = task_service.add_task("Task 1", "Description 1", "high")
        task2 = task_service.add_task("Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Task 3", "Description 3", "low")
        
        # Complete one task
        task_service.complete_task(task2.id)
        
        # Update one task
        task_service.update_task(task1.id, title="Updated Task 1", priority="medium")
        
        # Delete one task
        task_service.delete_task(task3.id)
        
        # Verify final state
        remaining_tasks = task_service.get_all_tasks()
        assert len(remaining_tasks) == 2
        
        # Check updated task
        updated_task = task_service.get_task_by_id(task1.id)
        assert updated_task.title == "Updated Task 1"
        assert updated_task.priority == "medium"
        
        # Check completed task
        completed_task = task_service.get_task_by_id(task2.id)
        assert completed_task.completed is True
        
        # Verify deleted task is gone
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(task3.id)