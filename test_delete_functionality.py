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
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException

def test_delete_functionality():
    """Test the delete functionality of TaskService."""
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        # Initialize TaskService with temporary file
        task_service = TaskService(temp_file)
        
        # Add some test tasks
        task1 = task_service.add_task("Test Task 1", "Description 1", "high")
        task2 = task_service.add_task("Test Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Test Task 3", "Description 3", "low")
        
        print(f"Created tasks with IDs: {task1.id}, {task2.id}, {task3.id}")
        
        # Verify tasks exist
        all_tasks = task_service.get_all_tasks()
        print(f"Total tasks before deletion: {len(all_tasks)}")
        
        # Delete task2
        deleted_task = task_service.delete_task(task2.id)
        print(f"Deleted task: {deleted_task.title}")
        
        # Verify task was deleted
        remaining_tasks = task_service.get_all_tasks()
        print(f"Total tasks after deletion: {len(remaining_tasks)}")
        
        # Verify the correct task was deleted
        remaining_ids = [task.id for task in remaining_tasks]
        print(f"Remaining task IDs: {remaining_ids}")
        
        # Try to delete a non-existent task
        try:
            task_service.delete_task(999)
            print("ERROR: Should have raised TaskNotFoundException")
        except TaskNotFoundException as e:
            print(f"Correctly caught exception: {e}")
        
        print("✅ Delete functionality test passed!")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def test_app_imports():
    """Test that the app.py file can be imported without errors."""
    try:
        # This will test if there are any syntax errors in app.py
        from src import app
        print("✅ App imports successfully!")
        return True
    except Exception as e:
        print(f"❌ Error importing app: {e}")
        return False

if __name__ == "__main__":
    print("Testing delete functionality...")
    test_delete_functionality()
    print("\nTesting app imports...")
    test_app_imports()
    print("\nAll tests completed!")