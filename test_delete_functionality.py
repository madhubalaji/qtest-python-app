#!/usr/bin/env python3
"""
Test script to verify the delete functionality works correctly.
"""

import os
import sys
import tempfile
import json

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


def test_delete_functionality():
    """Test the delete task functionality."""
    print("Testing delete task functionality...")
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        # Initialize task service with temporary file
        task_service = TaskService(temp_file)
        
        # Add some test tasks
        task1 = task_service.add_task("Test Task 1", "Description 1", "high")
        task2 = task_service.add_task("Test Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Test Task 3", "Description 3", "low")
        
        print(f"Created tasks with IDs: {task1.id}, {task2.id}, {task3.id}")
        
        # Verify all tasks exist
        all_tasks = task_service.get_all_tasks()
        print(f"Total tasks before deletion: {len(all_tasks)}")
        assert len(all_tasks) == 3, "Should have 3 tasks"
        
        # Delete the middle task
        deleted_task = task_service.delete_task(task2.id)
        print(f"Deleted task: {deleted_task.title}")
        
        # Verify task was deleted
        all_tasks = task_service.get_all_tasks()
        print(f"Total tasks after deletion: {len(all_tasks)}")
        assert len(all_tasks) == 2, "Should have 2 tasks after deletion"
        
        # Verify the correct task was deleted
        remaining_ids = [task.id for task in all_tasks]
        assert task1.id in remaining_ids, "Task 1 should still exist"
        assert task3.id in remaining_ids, "Task 3 should still exist"
        assert task2.id not in remaining_ids, "Task 2 should be deleted"
        
        # Try to delete a non-existent task
        try:
            task_service.delete_task(999)
            assert False, "Should have raised TaskNotFoundException"
        except TaskNotFoundException:
            print("Correctly raised TaskNotFoundException for non-existent task")
        
        # Verify data persistence
        task_service2 = TaskService(temp_file)
        persisted_tasks = task_service2.get_all_tasks()
        assert len(persisted_tasks) == 2, "Tasks should persist after service restart"
        
        print("✅ All delete functionality tests passed!")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_search_functionality():
    """Test that search functionality still works after our changes."""
    print("\nTesting search functionality...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        task_service = TaskService(temp_file)
        
        # Add test tasks
        task_service.add_task("Buy groceries", "Need milk and bread", "medium")
        task_service.add_task("Walk the dog", "Take Rex for a walk", "low")
        task_service.add_task("Finish project", "Complete the task manager", "high")
        
        # Test search
        results = task_service.search_tasks("dog")
        assert len(results) == 1, "Should find 1 task with 'dog'"
        assert results[0].title == "Walk the dog", "Should find the correct task"
        
        results = task_service.search_tasks("task")
        assert len(results) == 1, "Should find 1 task with 'task'"
        
        print("✅ Search functionality tests passed!")
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


if __name__ == "__main__":
    test_delete_functionality()
    test_search_functionality()
    print("\n🎉 All tests completed successfully!")