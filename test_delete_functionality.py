#!/usr/bin/env python3
"""
Quick test script to verify delete functionality works correctly.
"""

import os
import sys
import tempfile

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


def test_delete_functionality():
    """Test the delete functionality."""
    print("Testing delete functionality...")
    
    # Create a temporary file for testing
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()
    
    try:
        # Initialize task service
        task_service = TaskService(temp_file.name)
        
        # Add some test tasks
        print("Adding test tasks...")
        task1 = task_service.add_task("Task 1", "Description 1", "low")
        task2 = task_service.add_task("Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Task 3", "Description 3", "high")
        
        print(f"Added {len(task_service.tasks)} tasks")
        
        # Test deleting a task
        print(f"Deleting task with ID {task2.id}...")
        deleted_task = task_service.delete_task(task2.id)
        
        print(f"Deleted task: {deleted_task.title}")
        print(f"Remaining tasks: {len(task_service.tasks)}")
        
        # Verify the task was deleted
        remaining_tasks = task_service.get_all_tasks()
        task_ids = [task.id for task in remaining_tasks]
        
        assert task2.id not in task_ids, "Task was not deleted!"
        assert task1.id in task_ids, "Wrong task was deleted!"
        assert task3.id in task_ids, "Wrong task was deleted!"
        
        print("✓ Delete functionality works correctly!")
        
        # Test deleting non-existent task
        print("Testing deletion of non-existent task...")
        try:
            task_service.delete_task(999)
            print("✗ Should have raised TaskNotFoundException!")
            return False
        except TaskNotFoundException:
            print("✓ Correctly raised TaskNotFoundException for non-existent task!")
        
        # Test deleting all remaining tasks
        print("Deleting all remaining tasks...")
        for task in remaining_tasks:
            task_service.delete_task(task.id)
        
        assert len(task_service.get_all_tasks()) == 0, "Not all tasks were deleted!"
        print("✓ All tasks deleted successfully!")
        
        print("\n🎉 All delete functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        return False
        
    finally:
        # Clean up
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)


def test_app_syntax():
    """Test that the app.py file has no syntax errors."""
    print("Testing app.py syntax...")
    
    try:
        import src.app
        print("✓ app.py syntax is correct!")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in app.py: {e}")
        return False
    except Exception as e:
        print(f"✓ app.py syntax is correct (import error is expected: {e})")
        return True


if __name__ == "__main__":
    print("=" * 50)
    print("TESTING DELETE FUNCTIONALITY")
    print("=" * 50)
    
    syntax_ok = test_app_syntax()
    delete_ok = test_delete_functionality()
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"App syntax: {'✓ PASS' if syntax_ok else '✗ FAIL'}")
    print(f"Delete functionality: {'✓ PASS' if delete_ok else '✗ FAIL'}")
    
    if syntax_ok and delete_ok:
        print("\n🎉 All tests passed! Delete functionality is ready!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)