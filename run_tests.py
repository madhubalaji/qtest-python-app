#!/usr/bin/env python3
"""
Simple test runner to verify the test suite works correctly.
"""

import sys
import os
import subprocess

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

def run_tests():
    """Run the test suite and report results."""
    print("Running Task Manager Test Suite...")
    print("=" * 50)
    
    try:
        # Try to import the modules to check for import errors
        print("Checking imports...")
        from src.models.task import Task
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        print("✓ All imports successful")
        
        # Run a basic functionality test
        print("\nRunning basic functionality test...")
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Test basic operations
            service = TaskService(temp_file)
            
            # Add task
            task = service.add_task("Test Task", "Test Description", "high")
            assert task.id == 1
            assert task.title == "Test Task"
            print("✓ Add task works")
            
            # Get task
            retrieved = service.get_task_by_id(1)
            assert retrieved.title == "Test Task"
            print("✓ Get task works")
            
            # Delete task
            deleted = service.delete_task(1)
            assert deleted.title == "Test Task"
            assert len(service.tasks) == 0
            print("✓ Delete task works")
            
            # Test exception handling
            try:
                service.get_task_by_id(1)
                assert False, "Should have raised TaskNotFoundException"
            except TaskNotFoundException:
                print("✓ Exception handling works")
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        
        print("\n" + "=" * 50)
        print("✅ All basic tests passed!")
        print("The delete functionality has been successfully integrated.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)