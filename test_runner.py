#!/usr/bin/env python3
"""
Simple test runner to verify the setup works correctly.
"""

import sys
import os
import subprocess

def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing imports...")
    
    try:
        from src.models.task import Task
        print("✓ Task model imported successfully")
        
        from src.services.task_service import TaskService
        print("✓ TaskService imported successfully")
        
        from src.utils.exceptions import TaskNotFoundException
        print("✓ Exceptions imported successfully")
        
        from src.cli import main as cli_main
        print("✓ CLI module imported successfully")
        
        from src.app import main as app_main
        print("✓ Streamlit app imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of the Task and TaskService."""
    print("\nTesting basic functionality...")
    
    try:
        from src.models.task import Task
        from src.services.task_service import TaskService
        import tempfile
        import os
        
        # Test Task creation
        task = Task(1, "Test Task", "Test description", "high")
        print(f"✓ Task created: {task}")
        
        # Test TaskService with temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            service = TaskService(temp_file)
            added_task = service.add_task("Test Service Task", "Testing service", "medium")
            print(f"✓ Task added via service: {added_task}")
            
            tasks = service.get_all_tasks()
            print(f"✓ Retrieved {len(tasks)} tasks from service")
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        
        return True
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

def run_pytest():
    """Run pytest to execute the test suite."""
    print("\nRunning pytest...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Pytest execution failed: {e}")
        return False

def main():
    """Main test runner function."""
    print("=" * 60)
    print("Task Manager Test Runner")
    print("=" * 60)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test basic functionality
    if not test_basic_functionality():
        success = False
    
    # Run pytest
    if not run_pytest():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()