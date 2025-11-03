#!/usr/bin/env python3
"""
Test script to verify delete functionality works correctly.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def test_delete_functionality():
    """Test the delete functionality."""
    print("Testing delete functionality...")
    
    # Initialize task service
    config_dir = os.path.join("config")
    os.makedirs(config_dir, exist_ok=True)
    storage_file = os.path.join(config_dir, "tasks.json")
    task_service = TaskService(storage_file)
    
    # Show current tasks
    print("\nCurrent tasks:")
    tasks = task_service.get_all_tasks()
    for task in tasks:
        print(f"  ID: {task.id}, Title: {task.title}, Status: {'Completed' if task.completed else 'Active'}")
    
    if not tasks:
        print("No tasks found. Adding a test task...")
        task = task_service.add_task("Test Delete Task", "This task will be deleted", "low")
        print(f"Added task: {task.id} - {task.title}")
        tasks = task_service.get_all_tasks()
    
    # Test delete functionality
    if tasks:
        task_to_delete = tasks[0]
        print(f"\nTesting delete of task: {task_to_delete.id} - {task_to_delete.title}")
        
        try:
            deleted_task = task_service.delete_task(task_to_delete.id)
            print(f"✓ Successfully deleted task: {deleted_task.title}")
            
            # Verify task is gone
            remaining_tasks = task_service.get_all_tasks()
            if task_to_delete.id not in [t.id for t in remaining_tasks]:
                print("✓ Task successfully removed from storage")
            else:
                print("✗ Task still exists in storage")
                
        except TaskNotFoundException as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
    
    # Test deleting non-existent task
    print("\nTesting delete of non-existent task...")
    try:
        task_service.delete_task(99999)
        print("✗ Should have raised TaskNotFoundException")
    except TaskNotFoundException:
        print("✓ Correctly raised TaskNotFoundException for non-existent task")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    print("\nDelete functionality test completed!")

if __name__ == "__main__":
    test_delete_functionality()