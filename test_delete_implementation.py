#!/usr/bin/env python3
"""
Test script to verify the delete functionality implementation.
This script performs basic syntax and import validation.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

def test_syntax():
    """Test if the app.py file has valid Python syntax."""
    try:
        with open('src/app.py', 'r') as f:
            code = f.read()
        
        # Compile the code to check for syntax errors
        compile(code, 'src/app.py', 'exec')
        print("✅ Syntax validation passed")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in app.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        return False

def test_imports():
    """Test if all imports in the application work correctly."""
    try:
        # Test importing the main modules
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        from src.models.task import Task
        
        print("✅ Import validation passed")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        return False

def test_task_service():
    """Test basic TaskService functionality including delete method."""
    try:
        from src.services.task_service import TaskService
        
        # Create a temporary task service
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        service = TaskService(temp_file)
        
        # Test adding a task
        task = service.add_task("Test Task", "Test Description", "medium")
        print(f"✅ Task created with ID: {task.id}")
        
        # Test delete method exists and works
        deleted_task = service.delete_task(task.id)
        print(f"✅ Task deleted successfully: {deleted_task.title}")
        
        # Cleanup
        os.unlink(temp_file)
        
        return True
    except Exception as e:
        print(f"❌ TaskService test failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("🔍 Running validation tests for delete functionality implementation...\n")
    
    tests = [
        ("Syntax Validation", test_syntax),
        ("Import Validation", test_imports),
        ("TaskService Validation", test_task_service)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"VALIDATION SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validation tests passed! Delete functionality is ready.")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)