#!/usr/bin/env python3
"""
Simple test script to verify the delete functionality implementation.
"""

import sys
import os
import tempfile

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.models.task import Task
from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def test_basic_functionality():
    """Test basic task operations including delete."""
    print("Testing basic task functionality...")
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_file.write('[]')
        temp_file_path = temp_file.name
    
    try:
        # Initialize task service
        task_service = TaskService(temp_file_path)
        
        # Test adding tasks
        task1 = task_service.add_task("Test Task 1", "Description 1", "high")
        task2 = task_service.add_task("Test Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Test Task 3", "Description 3", "low")
        
        print(f"Added 3 tasks. Task IDs: {task1.id}, {task2.id}, {task3.id}")
        
        # Verify tasks were added
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == 3, f"Expected 3 tasks, got {len(all_tasks)}"
        print("✓ Tasks added successfully")
        
        # Test delete functionality
        deleted_task = task_service.delete_task(task2.id)
        assert deleted_task.id == task2.id, "Deleted task ID mismatch"
        print(f"✓ Deleted task {task2.id} successfully")
        
        # Verify task was deleted
        remaining_tasks = task_service.get_all_tasks()
        assert len(remaining_tasks) == 2, f"Expected 2 tasks after deletion, got {len(remaining_tasks)}"
        
        # Verify correct tasks remain
        remaining_ids = [task.id for task in remaining_tasks]
        assert task1.id in remaining_ids, "Task 1 should still exist"
        assert task3.id in remaining_ids, "Task 3 should still exist"
        assert task2.id not in remaining_ids, "Task 2 should be deleted"
        print("✓ Task deletion verified")
        
        # Test deleting non-existent task
        try:
            task_service.delete_task(999)
            assert False, "Should have raised TaskNotFoundException"
        except TaskNotFoundException:
            print("✓ TaskNotFoundException raised correctly for non-existent task")
        
        # Test task model equality and hashing
        test_task1 = Task(1, "Test", "Desc", "high")
        test_task2 = Task(1, "Test", "Desc", "high")
        test_task3 = Task(2, "Test", "Desc", "high")
        
        assert test_task1 == test_task2, "Equal tasks should be equal"
        assert test_task1 != test_task3, "Different tasks should not be equal"
        assert hash(test_task1) == hash(test_task2), "Equal tasks should have same hash"
        print("✓ Task equality and hashing work correctly")
        
        print("\n🎉 All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_app_imports():
    """Test that app imports work correctly."""
    print("\nTesting app imports...")
    
    try:
        from src.app import main, display_tasks_page, add_task_page, search_tasks_page
        print("✓ App functions imported successfully")
        
        # Test that streamlit functions are available (they should be mocked in tests)
        import streamlit as st
        print("✓ Streamlit imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running implementation verification tests...\n")
    
    basic_test_passed = test_basic_functionality()
    import_test_passed = test_app_imports()
    
    if basic_test_passed and import_test_passed:
        print("\n✅ All verification tests passed! The implementation looks good.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)