#!/usr/bin/env python3
"""
Demo script to showcase the delete functionality.
"""

import sys
import os
import tempfile

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def demo_delete_functionality():
    """Demonstrate the delete functionality."""
    print("🎯 Task Manager Delete Functionality Demo")
    print("=" * 50)
    
    # Create a temporary storage file
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()
    
    try:
        # Initialize task service
        task_service = TaskService(temp_file.name)
        
        # Add some sample tasks
        print("\n📝 Adding sample tasks...")
        task1 = task_service.add_task("Learn Python", "Complete Python tutorial", "high")
        task2 = task_service.add_task("Build Web App", "Create a Streamlit application", "medium")
        task3 = task_service.add_task("Write Tests", "Add comprehensive test coverage", "low")
        
        print(f"✅ Added task: {task1}")
        print(f"✅ Added task: {task2}")
        print(f"✅ Added task: {task3}")
        
        # Show all tasks
        print(f"\n📋 Total tasks: {len(task_service.get_all_tasks())}")
        for task in task_service.get_all_tasks():
            print(f"   - {task}")
        
        # Delete a task
        print(f"\n🗑️ Deleting task with ID {task2.id}: '{task2.title}'")
        deleted_task = task_service.delete_task(task2.id)
        print(f"✅ Successfully deleted: {deleted_task}")
        
        # Show remaining tasks
        print(f"\n📋 Remaining tasks: {len(task_service.get_all_tasks())}")
        for task in task_service.get_all_tasks():
            print(f"   - {task}")
        
        # Try to delete a non-existent task
        print(f"\n🚫 Attempting to delete non-existent task (ID: 999)...")
        try:
            task_service.delete_task(999)
        except TaskNotFoundException as e:
            print(f"✅ Correctly caught exception: {e}")
        
        # Delete remaining tasks
        print(f"\n🗑️ Deleting remaining tasks...")
        for task in task_service.get_all_tasks().copy():
            deleted = task_service.delete_task(task.id)
            print(f"✅ Deleted: {deleted.title}")
        
        print(f"\n📋 Final task count: {len(task_service.get_all_tasks())}")
        
        print("\n🎉 Delete functionality demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        raise
    finally:
        # Cleanup
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
            print(f"🧹 Cleaned up temporary file: {temp_file.name}")

if __name__ == "__main__":
    demo_delete_functionality()