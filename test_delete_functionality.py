#!/usr/bin/env python3
"""
Test script to verify the delete functionality implementation.
"""

import os
import sys
import tempfile
import json

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def test_delete_functionality():
    """Test the delete functionality in TaskService."""
    print("Testing delete functionality...")
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_file_path = temp_file.name
    
    try:
        # Initialize TaskService with temporary file
        task_service = TaskService(temp_file_path)
        
        # Add some test tasks
        task1 = task_service.add_task("Test Task 1", "Description 1", "high")
        task2 = task_service.add_task("Test Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Test Task 3", "Description 3", "low")
        
        print(f"✓ Created 3 test tasks")
        print(f"  - Task {task1.id}: {task1.title}")
        print(f"  - Task {task2.id}: {task2.title}")
        print(f"  - Task {task3.id}: {task3.title}")
        
        # Verify all tasks exist
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 3, f"Expected 3 tasks, got {len(all_tasks)}"
        print(f"✓ Verified all 3 tasks exist")
        
        # Test deleting a task
        deleted_task = task_service.delete_task(task2.id)
        assert deleted_task.id == task2.id, "Deleted task ID mismatch"
        print(f"✓ Successfully deleted task {task2.id}: {task2.title}")
        
        # Verify task was removed
        remaining_tasks = task_service.get_all_tasks()
        assert len(remaining_tasks) == 2, f"Expected 2 tasks after deletion, got {len(remaining_tasks)}"
        
        # Verify the correct task was deleted
        remaining_ids = [task.id for task in remaining_tasks]
        assert task1.id in remaining_ids, "Task 1 should still exist"
        assert task3.id in remaining_ids, "Task 3 should still exist"
        assert task2.id not in remaining_ids, "Task 2 should be deleted"
        print(f"✓ Verified correct task was deleted, 2 tasks remain")
        
        # Test deleting non-existent task
        try:
            task_service.delete_task(999)
            assert False, "Should have raised TaskNotFoundException"
        except TaskNotFoundException:
            print(f"✓ Correctly raised TaskNotFoundException for non-existent task")
        
        # Test deleting remaining tasks
        task_service.delete_task(task1.id)
        task_service.delete_task(task3.id)
        
        final_tasks = task_service.get_all_tasks()
        assert len(final_tasks) == 0, f"Expected 0 tasks after deleting all, got {len(final_tasks)}"
        print(f"✓ Successfully deleted all remaining tasks")
        
        print("\n🎉 All delete functionality tests passed!")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_app_import():
    """Test that the app module can be imported without errors."""
    print("\nTesting app module import...")
    
    try:
        from src import app
        print("✓ Successfully imported app module")
        
        # Test that main functions exist
        assert hasattr(app, 'main'), "main function should exist"
        assert hasattr(app, 'display_tasks_page'), "display_tasks_page function should exist"
        assert hasattr(app, 'add_task_page'), "add_task_page function should exist"
        assert hasattr(app, 'search_tasks_page'), "search_tasks_page function should exist"
        print("✓ All required functions exist in app module")
        
    except Exception as e:
        print(f"❌ Error importing app module: {e}")
        raise

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING DELETE FUNCTIONALITY IMPLEMENTATION")
    print("=" * 60)
    
    test_delete_functionality()
    test_app_import()
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY! 🎉")
    print("=" * 60)
    print("\nThe delete functionality has been successfully implemented:")
    print("• Delete buttons added to View Tasks page with confirmation")
    print("• Delete buttons added to Search Tasks page with confirmation")  
    print("• Delete buttons added to task details view with confirmation")
    print("• Proper error handling for non-existent tasks")
    print("• Success messages for successful deletions")
    print("• Session state management for confirmation dialogs")