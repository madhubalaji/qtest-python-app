#!/usr/bin/env python3
"""
Test script to verify delete functionality.
This script tests the delete_task method and ensures proper integration.
"""

import os
import sys
import tempfile
import json

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException


def test_delete_task():
    """Test the delete task functionality."""
    print("Testing delete task functionality...")
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
        json.dump([], f)
    
    try:
        # Initialize task service
        task_service = TaskService(temp_file)
        
        # Add some test tasks
        print("\n1. Adding test tasks...")
        task1 = task_service.add_task("Task 1", "Description 1", "high")
        task2 = task_service.add_task("Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Task 3", "Description 3", "low")
        
        print(f"   Added task 1 with ID: {task1.id}")
        print(f"   Added task 2 with ID: {task2.id}")
        print(f"   Added task 3 with ID: {task3.id}")
        
        # Verify all tasks exist
        all_tasks = task_service.get_all_tasks()
        print(f"\n2. Total tasks before deletion: {len(all_tasks)}")
        assert len(all_tasks) == 3, "Expected 3 tasks"
        
        # Delete task 2
        print(f"\n3. Deleting task with ID {task2.id}...")
        deleted_task = task_service.delete_task(task2.id)
        print(f"   Deleted task: {deleted_task.title}")
        
        # Verify task is deleted
        all_tasks = task_service.get_all_tasks()
        print(f"\n4. Total tasks after deletion: {len(all_tasks)}")
        assert len(all_tasks) == 2, "Expected 2 tasks after deletion"
        
        # Verify the correct task was deleted
        remaining_ids = [task.id for task in all_tasks]
        print(f"   Remaining task IDs: {remaining_ids}")
        assert task2.id not in remaining_ids, "Deleted task should not be in list"
        assert task1.id in remaining_ids, "Task 1 should still exist"
        assert task3.id in remaining_ids, "Task 3 should still exist"
        
        # Try to get deleted task (should raise exception)
        print(f"\n5. Attempting to retrieve deleted task...")
        try:
            task_service.get_task_by_id(task2.id)
            print("   ERROR: Should have raised TaskNotFoundException")
            assert False, "Should have raised TaskNotFoundException"
        except TaskNotFoundException as e:
            print(f"   ✓ Correctly raised exception: {e}")
        
        # Try to delete non-existent task
        print(f"\n6. Attempting to delete non-existent task...")
        try:
            task_service.delete_task(999)
            print("   ERROR: Should have raised TaskNotFoundException")
            assert False, "Should have raised TaskNotFoundException"
        except TaskNotFoundException as e:
            print(f"   ✓ Correctly raised exception: {e}")
        
        # Verify persistence (reload from file)
        print("\n7. Testing persistence (reloading from file)...")
        task_service_reload = TaskService(temp_file)
        reloaded_tasks = task_service_reload.get_all_tasks()
        print(f"   Reloaded {len(reloaded_tasks)} tasks from file")
        assert len(reloaded_tasks) == 2, "Expected 2 tasks after reload"
        
        reloaded_ids = [task.id for task in reloaded_tasks]
        assert task2.id not in reloaded_ids, "Deleted task should not be in reloaded data"
        
        print("\n✅ All delete functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"\nCleaned up temporary file: {temp_file}")


def test_ui_integration():
    """Test UI integration points."""
    print("\n" + "="*60)
    print("Testing UI Integration...")
    print("="*60)
    
    # Check that app.py has the required components
    app_file = os.path.join(os.path.dirname(__file__), 'src', 'app.py')
    
    with open(app_file, 'r') as f:
        app_content = f.read()
    
    print("\n1. Checking for delete button in View Tasks page...")
    assert '🗑️' in app_content, "Delete button emoji not found"
    assert 'delete_confirm_id' in app_content, "Delete confirmation state not found"
    print("   ✓ Delete button present")
    
    print("\n2. Checking for confirmation dialog...")
    assert 'Are you sure you want to delete' in app_content, "Confirmation message not found"
    assert 'Yes, Delete' in app_content, "Confirm button not found"
    assert 'Cancel' in app_content, "Cancel button not found"
    print("   ✓ Confirmation dialog present")
    
    print("\n3. Checking for delete in search results...")
    assert 'delete_search_' in app_content, "Delete button in search not found"
    print("   ✓ Delete in search results present")
    
    print("\n4. Checking for delete in task details view...")
    assert 'Delete Task' in app_content, "Delete button in details not found"
    print("   ✓ Delete in task details present")
    
    print("\n5. Checking for proper state cleanup...")
    assert 'del st.session_state.delete_confirm_id' in app_content, "State cleanup not found"
    print("   ✓ State cleanup present")
    
    print("\n6. Checking for task_service.delete_task() calls...")
    assert 'task_service.delete_task(' in app_content, "Delete service call not found"
    print("   ✓ Service integration present")
    
    print("\n✅ All UI integration checks passed!")
    return True


if __name__ == "__main__":
    print("="*60)
    print("DELETE TASK FUNCTIONALITY TEST SUITE")
    print("="*60)
    
    test1_passed = test_delete_task()
    test2_passed = test_ui_integration()
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Backend Tests: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"UI Integration Tests: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
