#!/usr/bin/env python3
"""
Validation script to check the implementation for syntax errors and basic functionality.
"""

import os
import sys
import tempfile

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

def validate_imports():
    """Validate that all modules can be imported without syntax errors."""
    print("Validating imports...")
    
    try:
        # Test importing the models
        from src.models.task import Task
        print("✓ Task model imported successfully")
        
        # Test importing the services
        from src.services.task_service import TaskService
        print("✓ TaskService imported successfully")
        
        # Test importing exceptions
        from src.utils.exceptions import TaskNotFoundException
        print("✓ TaskNotFoundException imported successfully")
        
        # Test importing the main app (this might fail due to Streamlit, but syntax should be OK)
        try:
            import src.app
            print("✓ Main app imported successfully")
        except ImportError as e:
            if "streamlit" in str(e).lower():
                print("✓ Main app syntax is correct (Streamlit not available)")
            else:
                print(f"✗ Main app import failed: {e}")
                return False
        
        return True
        
    except SyntaxError as e:
        print(f"✗ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def validate_delete_functionality():
    """Validate the delete functionality works correctly."""
    print("\nValidating delete functionality...")
    
    # Create a temporary file for testing
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()
    
    try:
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        
        # Initialize task service
        task_service = TaskService(temp_file.name)
        
        # Add test tasks
        task1 = task_service.add_task("Test Task 1", "Description 1", "low")
        task2 = task_service.add_task("Test Task 2", "Description 2", "medium")
        task3 = task_service.add_task("Test Task 3", "Description 3", "high")
        
        initial_count = len(task_service.tasks)
        print(f"✓ Added {initial_count} test tasks")
        
        # Test deleting a task
        deleted_task = task_service.delete_task(task2.id)
        remaining_count = len(task_service.tasks)
        
        if remaining_count == initial_count - 1:
            print("✓ Task deleted successfully")
        else:
            print(f"✗ Expected {initial_count - 1} tasks, got {remaining_count}")
            return False
        
        if deleted_task.id == task2.id:
            print("✓ Correct task was deleted")
        else:
            print(f"✗ Wrong task deleted. Expected ID {task2.id}, got {deleted_task.id}")
            return False
        
        # Test deleting non-existent task
        try:
            task_service.delete_task(999)
            print("✗ Should have raised TaskNotFoundException")
            return False
        except TaskNotFoundException:
            print("✓ TaskNotFoundException raised correctly for non-existent task")
        
        # Test that remaining tasks are correct
        remaining_tasks = task_service.get_all_tasks()
        remaining_ids = [task.id for task in remaining_tasks]
        
        if task1.id in remaining_ids and task3.id in remaining_ids and task2.id not in remaining_ids:
            print("✓ Correct tasks remain after deletion")
        else:
            print(f"✗ Incorrect tasks remaining. Expected [{task1.id}, {task3.id}], got {remaining_ids}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Delete functionality test failed: {e}")
        return False
        
    finally:
        # Clean up
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

def validate_task_model():
    """Validate the Task model functionality."""
    print("\nValidating Task model...")
    
    try:
        from src.models.task import Task
        
        # Test task creation
        task = Task(1, "Test Task", "Test Description", "high", False)
        print("✓ Task creation successful")
        
        # Test to_dict
        task_dict = task.to_dict()
        if isinstance(task_dict, dict) and 'id' in task_dict:
            print("✓ Task to_dict method works")
        else:
            print("✗ Task to_dict method failed")
            return False
        
        # Test from_dict
        restored_task = Task.from_dict(task_dict)
        if restored_task.id == task.id and restored_task.title == task.title:
            print("✓ Task from_dict method works")
        else:
            print("✗ Task from_dict method failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Task model validation failed: {e}")
        return False

def main():
    """Main validation function."""
    print("=" * 60)
    print("IMPLEMENTATION VALIDATION")
    print("=" * 60)
    
    results = []
    
    # Run all validations
    results.append(("Imports", validate_imports()))
    results.append(("Task Model", validate_task_model()))
    results.append(("Delete Functionality", validate_delete_functionality()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:20}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("The delete functionality has been successfully implemented!")
    else:
        print("❌ SOME VALIDATIONS FAILED!")
        print("Please review the errors above.")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)