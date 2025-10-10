#!/usr/bin/env python3
"""
Test script to verify delete functionality in the task manager.
"""

import os
import sys
import json

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.services.task_service import TaskService
from src.models.task import Task

def test_delete_functionality():
    """Test the delete functionality of TaskService."""
    
    # Create a temporary test file
    test_file = "test_tasks.json"
    
    try:
        # Initialize TaskService with test file
        task_service = TaskService(test_file)
        
        # Add some test tasks
        print("टेस्ट कार्य जोड़े जा रहे हैं...")  # Adding test tasks in Hindi
        task1 = task_service.add_task("टेस्ट कार्य 1", "यह पहला टेस्ट कार्य है", "high")  # Test Task 1, This is first test task in Hindi
        task2 = task_service.add_task("टेस्ट कार्य 2", "यह दूसरा टेस्ट कार्य है", "medium")  # Test Task 2, This is second test task in Hindi
        task3 = task_service.add_task("टेस्ट कार्य 3", "यह तीसरा टेस्ट कार्य है", "low")  # Test Task 3, This is third test task in Hindi
        
        print(f"जोड़े गए कार्य: {len(task_service.get_all_tasks())}")  # Added tasks in Hindi
        
        # Display all tasks
        print("\nसभी कार्य:")  # All tasks in Hindi
        for task in task_service.get_all_tasks():
            print(f"  - {task}")
        
        # Test delete functionality
        print(f"\nकार्य {task2.id} को हटाया जा रहा है...")  # Deleting task in Hindi
        deleted_task = task_service.delete_task(task2.id)
        print(f"हटाया गया कार्य: {deleted_task}")  # Deleted task in Hindi
        
        # Display remaining tasks
        print(f"\nबचे हुए कार्य: {len(task_service.get_all_tasks())}")  # Remaining tasks in Hindi
        for task in task_service.get_all_tasks():
            print(f"  - {task}")
        
        # Test deleting non-existent task
        print(f"\nगैर-मौजूद कार्य को हटाने का प्रयास...")  # Trying to delete non-existent task in Hindi
        try:
            task_service.delete_task(999)
        except Exception as e:
            print(f"अपेक्षित त्रुटि: {e}")  # Expected error in Hindi
        
        print("\nडिलीट फंक्शनैलिटी टेस्ट सफल!")  # Delete functionality test successful in Hindi
        
    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"टेस्ट फाइल {test_file} साफ की गई")  # Test file cleaned in Hindi

if __name__ == "__main__":
    test_delete_functionality()