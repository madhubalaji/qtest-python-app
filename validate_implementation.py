#!/usr/bin/env python3
"""
Validate the delete functionality implementation.
"""

import os
import sys
import tempfile

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from src.services.task_service import TaskService
        from src.models.task import Task
        from src.utils.exceptions import TaskNotFoundException
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_delete_functionality():
    """Test the delete functionality."""
    try:
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Initialize TaskService
            task_service = TaskService(temp_file)
            
            # Add test tasks
            task1 = task_service.add_task("Test Task 1", "Description 1", "high")
            task2 = task_service.add_task("Test Task 2", "Description 2", "medium")
            
            print(f"Created tasks: {task1.id}, {task2.id}")
            
            # Delete one task
            deleted_task = task_service.delete_task(task1.id)
            print(f"Deleted task: {deleted_task.title}")
            
            # Verify deletion
            remaining_tasks = task_service.get_all_tasks()
            print(f"Remaining tasks: {len(remaining_tasks)}")
            
            # Test exception for non-existent task
            try:
                task_service.delete_task(999)
                print("❌ Should have raised exception")
                return False
            except TaskNotFoundException:
                print("✅ Exception handling works")
            
            print("✅ Delete functionality works correctly")
            return True
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        print(f"❌ Delete test error: {e}")
        return False

def test_app_syntax():
    """Test that app.py has no syntax errors."""
    try:
        # Try to compile the app.py file
        with open('src/app.py', 'r') as f:
            code = f.read()
        
        compile(code, 'src/app.py', 'exec')
        print("✅ App.py syntax is valid")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in app.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking app.py: {e}")
        return False

def main():
    """Run all validation tests."""
    print("Validating delete functionality implementation...")
    print()
    
    tests = [
        ("Import Test", test_imports),
        ("Delete Functionality Test", test_delete_functionality),
        ("App Syntax Test", test_app_syntax),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    if all(results):
        print("🎉 All validation tests passed!")
        print("The delete functionality has been successfully implemented.")
    else:
        print("❌ Some validation tests failed.")
        
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)