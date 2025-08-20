#!/usr/bin/env python3
"""
Simple test runner to verify the delete functionality works.
"""

import sys
import os
import tempfile

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def test_delete_functionality():
    """Test the delete functionality manually."""
    print("Testing Task Delete Functionality...")
    print("=" * 50)
    
    # Create a temporary file for testing
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()
    
    try:
        # Initialize task service
        task_service = TaskService(temp_file.name)
        
        # Test 1: Add and delete a single task
        print("\n1. Testing single task deletion...")
        task = task_service.add_task("Test Task", "Test Description", "high")
        print(f"   Added task: {task.title} (ID: {task.id})")
        
        deleted_task = task_service.delete_task(task.id)
        print(f"   Deleted task: {deleted_task.title} (ID: {deleted_task.id})")
        
        remaining_tasks = task_service.get_all_tasks()
        print(f"   Remaining tasks: {len(remaining_tasks)}")
        assert len(remaining_tasks) == 0, "Task was not deleted properly"
        print("   ✓ Single task deletion works!")
        
        # Test 2: Delete from multiple tasks
        print("\n2. Testing deletion from multiple tasks...")
        task1 = task_service.add_task("Task 1", "Description 1", "low")
        task2 = task_service.add_task("Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Task 3", "Description 3", "high")
        print(f"   Added 3 tasks (IDs: {task1.id}, {task2.id}, {task3.id})")
        
        # Delete middle task
        deleted_task = task_service.delete_task(task2.id)
        print(f"   Deleted middle task: {deleted_task.title}")
        
        remaining_tasks = task_service.get_all_tasks()
        remaining_ids = [task.id for task in remaining_tasks]
        print(f"   Remaining task IDs: {remaining_ids}")
        
        assert len(remaining_tasks) == 2, "Wrong number of tasks remaining"
        assert task1.id in remaining_ids, "Task 1 should still exist"
        assert task3.id in remaining_ids, "Task 3 should still exist"
        assert task2.id not in remaining_ids, "Task 2 should be deleted"
        print("   ✓ Multiple task deletion works!")
        
        # Test 3: Delete non-existent task
        print("\n3. Testing deletion of non-existent task...")
        try:
            task_service.delete_task(999)
            assert False, "Should have raised TaskNotFoundException"
        except TaskNotFoundException as e:
            print(f"   ✓ Correctly raised exception: {e}")
        
        # Test 4: Delete completed task
        print("\n4. Testing deletion of completed task...")
        task_service.complete_task(task1.id)
        completed_task = task_service.get_task_by_id(task1.id)
        assert completed_task.completed, "Task should be completed"
        
        deleted_task = task_service.delete_task(task1.id)
        print(f"   Deleted completed task: {deleted_task.title}")
        assert deleted_task.completed, "Deleted task should have been completed"
        print("   ✓ Completed task deletion works!")
        
        # Test 5: Persistence test
        print("\n5. Testing persistence...")
        task_service.add_task("Persistent Task", "Test persistence", "medium")
        
        # Create new service instance
        new_service = TaskService(temp_file.name)
        tasks_before = len(new_service.get_all_tasks())
        print(f"   Tasks before deletion: {tasks_before}")
        
        # Delete using new service
        task_to_delete = new_service.get_all_tasks()[0]
        new_service.delete_task(task_to_delete.id)
        
        # Create another service instance
        another_service = TaskService(temp_file.name)
        tasks_after = len(another_service.get_all_tasks())
        print(f"   Tasks after deletion: {tasks_after}")
        
        assert tasks_after == tasks_before - 1, "Deletion not persisted"
        print("   ✓ Persistence works!")
        
        print("\n" + "=" * 50)
        print("🎉 All delete functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

if __name__ == '__main__':
    success = test_delete_functionality()
    sys.exit(0 if success else 1)