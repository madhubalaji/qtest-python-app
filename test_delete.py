#!/usr/bin/env python3
"""
Simple test script to verify the delete functionality works correctly.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def test_delete_functionality():
    """Test the delete task functionality."""
    print("Testing delete task functionality...")
    
    # Initialize task service
    config_dir = os.path.join("config")
    storage_file = os.path.join(config_dir, "tasks.json")
    task_service = TaskService(storage_file)
    
    # Display current tasks
    print("\nCurrent tasks:")
    tasks = task_service.get_all_tasks()
    for task in tasks:
        print(f"  - ID: {task.id}, Title: {task.title}, Completed: {task.completed}")
    
    if not tasks:
        print("No tasks found. Adding a test task...")
        task = task_service.add_task("Test Delete Task", "This task will be deleted", "low")
        print(f"Added task: {task.title} with ID {task.id}")
        tasks = task_service.get_all_tasks()
    
    # Test deleting the first task
    if tasks:
        task_to_delete = tasks[0]
        print(f"\nDeleting task: {task_to_delete.title} (ID: {task_to_delete.id})")
        
        try:
            deleted_task = task_service.delete_task(task_to_delete.id)
            print(f"Successfully deleted task: {deleted_task.title}")
            
            # Verify the task is gone
            remaining_tasks = task_service.get_all_tasks()
            print(f"\nRemaining tasks: {len(remaining_tasks)}")
            for task in remaining_tasks:
                print(f"  - ID: {task.id}, Title: {task.title}")
                
        except TaskNotFoundException as e:
            print(f"Error: {e}")
    
    print("\nDelete functionality test completed!")

if __name__ == "__main__":
    test_delete_functionality()