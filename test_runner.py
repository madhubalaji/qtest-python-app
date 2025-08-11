#!/usr/bin/env python3
"""
Simple test runner to check our implementation.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('/workspace'))

def test_imports():
    """Test that all imports work."""
    print("Testing imports...")
    try:
        from src.models.task import Task
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic task service functionality including delete."""
    print("\nTesting basic functionality...")
    try:
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        import tempfile
        import os
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Test TaskService
            service = TaskService(temp_file)
            
            # Add tasks
            task1 = service.add_task("Test Task 1", "Description 1", "high")
            task2 = service.add_task("Test Task 2", "Description 2", "medium")
            
            print(f"✓ Added 2 tasks, got IDs: {task1.id}, {task2.id}")
            
            # Test delete functionality
            deleted_task = service.delete_task(task1.id)
            print(f"✓ Deleted task: {deleted_task.title}")
            
            # Verify task is gone
            remaining_tasks = service.get_all_tasks()
            print(f"✓ Remaining tasks: {len(remaining_tasks)}")
            
            # Try to get deleted task (should raise exception)
            try:
                service.get_task_by_id(task1.id)
                print("✗ ERROR: Deleted task still accessible")
                return False
            except TaskNotFoundException:
                print("✓ Deleted task properly removed")
            
            # Test search after delete
            results = service.search_tasks("Test Task 1")
            if len(results) == 0:
                print("✓ Search doesn't find deleted task")
            else:
                print("✗ ERROR: Search found deleted task")
                return False
            
            return True
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        print(f"✗ Functionality test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_task_model():
    """Test task model functionality."""
    print("\nTesting Task model...")
    try:
        from src.models.task import Task
        
        # Create task
        task = Task(1, "Test Task", "Test Description", "high")
        print(f"✓ Created task: {task}")
        
        # Test serialization
        task_dict = task.to_dict()
        print(f"✓ Serialized to dict: {task_dict}")
        
        # Test deserialization
        task2 = Task.from_dict(task_dict)
        print(f"✓ Deserialized from dict: {task2}")
        
        return True
        
    except Exception as e:
        print(f"✗ Task model test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running implementation tests...\n")
    
    success = True
    success &= test_imports()
    success &= test_task_model()
    success &= test_basic_functionality()
    
    if success:
        print("\n🎉 All tests passed! Delete functionality is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")