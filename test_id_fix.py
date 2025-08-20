#!/usr/bin/env python3
"""
Quick test to verify ID reuse fix is working.
"""

import os
import sys
import tempfile

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.services.task_service import TaskService


def test_id_reuse_fix():
    """Test that task IDs are not reused after deletion."""
    # Create a temporary file for testing
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()
    
    try:
        # Initialize task service
        task_service = TaskService(temp_file.name)
        
        # Add a task
        task1 = task_service.add_task("First Task", "Description", "low")
        first_id = task1.id
        print(f"Added first task with ID: {first_id}")
        
        # Delete the task
        task_service.delete_task(first_id)
        print(f"Deleted task with ID: {first_id}")
        
        # Add a new task
        task2 = task_service.add_task("Second Task", "Description", "medium")
        second_id = task2.id
        print(f"Added second task with ID: {second_id}")
        
        # Verify the new task has a different ID
        if first_id != second_id:
            print(f"✅ SUCCESS: IDs are different ({first_id} != {second_id})")
            return True
        else:
            print(f"❌ FAILURE: IDs are the same ({first_id} == {second_id})")
            return False
            
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)


if __name__ == '__main__':
    success = test_id_reuse_fix()
    sys.exit(0 if success else 1)