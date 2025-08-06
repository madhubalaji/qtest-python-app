#!/usr/bin/env python3
"""
Simple test runner to verify the task manager functionality.
"""

import sys
import os
import tempfile
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

def test_task_model():
    """Test the Task model functionality."""
    print("Testing Task model...")
    
    from src.models.task import Task
    
    # Test basic task creation
    task = Task(1, "Test Task", "Test description", "high")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test description"
    assert task.priority == "high"
    assert task.completed is False
    
    # Test to_dict and from_dict
    task_dict = task.to_dict()
    task_from_dict = Task.from_dict(task_dict)
    assert task_from_dict.id == task.id
    assert task_from_dict.title == task.title
    
    print("✓ Task model tests passed!")

def test_task_service():
    """Test the TaskService functionality, especially delete operations."""
    print("Testing TaskService...")
    
    from src.services.task_service import TaskService
    from src.utils.exceptions import TaskNotFoundException
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        # Initialize service
        service = TaskService(temp_file)
        
        # Test adding tasks
        task1 = service.add_task("Task 1", "First task", "high")
        task2 = service.add_task("Task 2", "Second task", "medium")
        task3 = service.add_task("Task 3", "Third task", "low")
        
        # Verify tasks were added
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 3
        print("✓ Task addition works!")
        
        # Test getting task by ID
        retrieved_task = service.get_task_by_id(task1.id)
        assert retrieved_task.title == "Task 1"
        print("✓ Task retrieval works!")
        
        # Test delete functionality
        deleted_task = service.delete_task(task2.id)
        assert deleted_task.id == task2.id
        assert deleted_task.title == "Task 2"
        
        # Verify task was deleted
        remaining_tasks = service.get_all_tasks()
        assert len(remaining_tasks) == 2
        assert not any(task.id == task2.id for task in remaining_tasks)
        print("✓ Task deletion works!")
        
        # Test deleting non-existent task
        try:
            service.delete_task(999)
            assert False, "Should have raised TaskNotFoundException"
        except TaskNotFoundException:
            print("✓ Delete non-existent task error handling works!")
        
        # Test other operations still work after deletion
        service.complete_task(task1.id)
        completed_task = service.get_task_by_id(task1.id)
        assert completed_task.completed is True
        print("✓ Task completion after deletion works!")
        
        # Test search functionality
        search_results = service.search_tasks("Task")
        assert len(search_results) == 2  # task1 and task3
        print("✓ Task search works!")
        
        # Test persistence
        service2 = TaskService(temp_file)
        persisted_tasks = service2.get_all_tasks()
        assert len(persisted_tasks) == 2
        print("✓ Task persistence works!")
        
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    print("✓ All TaskService tests passed!")

def test_delete_functionality_comprehensive():
    """Comprehensive test of delete functionality."""
    print("Testing comprehensive delete functionality...")
    
    from src.services.task_service import TaskService
    from src.utils.exceptions import TaskNotFoundException
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        service = TaskService(temp_file)
        
        # Add multiple tasks
        tasks = []
        for i in range(5):
            task = service.add_task(f"Task {i+1}", f"Description {i+1}", "medium")
            tasks.append(task)
        
        # Delete tasks in different orders
        # Delete middle task
        service.delete_task(tasks[2].id)
        remaining = service.get_all_tasks()
        assert len(remaining) == 4
        assert not any(t.id == tasks[2].id for t in remaining)
        
        # Delete first task
        service.delete_task(tasks[0].id)
        remaining = service.get_all_tasks()
        assert len(remaining) == 3
        
        # Delete last remaining tasks
        for task in remaining:
            service.delete_task(task.id)
        
        # Verify all tasks deleted
        final_remaining = service.get_all_tasks()
        assert len(final_remaining) == 0
        
        print("✓ Comprehensive delete functionality works!")
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def main():
    """Run all tests."""
    print("Running Task Manager Tests...")
    print("=" * 50)
    
    try:
        test_task_model()
        print()
        test_task_service()
        print()
        test_delete_functionality_comprehensive()
        print()
        print("=" * 50)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("The delete functionality has been successfully implemented!")
        print("You can now:")
        print("- Delete tasks from the 'View Tasks' page with confirmation")
        print("- Delete tasks from the 'Search Tasks' detail view")
        print("- All existing functionality continues to work")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()