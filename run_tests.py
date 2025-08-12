"""
Test runner script for the task manager application.
"""

import sys
import os
import subprocess

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_pytest():
    """Run pytest with appropriate configuration."""
    try:
        # Run pytest
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', '-v', '--tb=short'
        ], capture_output=True, text=True)
        
        print("PYTEST OUTPUT:")
        print(result.stdout)
        if result.stderr:
            print("PYTEST ERRORS:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running pytest: {e}")
        return False

def run_simple_tests():
    """Run simple test scripts."""
    try:
        from src.models.task import Task
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        
        print("Running simple functionality tests...")
        
        # Test basic functionality
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write('[]')
            temp_file = f.name
        
        try:
            service = TaskService(temp_file)
            
            # Test the specific scenario from the failing test
            # Add initial tasks
            task1 = service.add_task("Task 1")
            task2 = service.add_task("Task 2") 
            task3 = service.add_task("Task 3")
            
            print(f"Initial tasks: {task1.id}, {task2.id}, {task3.id}")
            
            # Delete tasks 1 and 3
            service.delete_task(1)
            service.delete_task(3)
            
            # Add new task
            new_task = service.add_task("New Task")
            print(f"New task ID after deletions: {new_task.id}")
            
            # This should be 4 according to the test expectation
            if new_task.id == 4:
                print("✓ ID generation test passed!")
                return True
            else:
                print(f"✗ ID generation test failed! Expected 4, got {new_task.id}")
                return False
                
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"✗ Simple test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running Task Manager Tests...")
    
    # Run simple tests first
    simple_passed = run_simple_tests()
    
    print("\n" + "="*50)
    
    # Run pytest
    pytest_passed = run_pytest()
    
    print("\n" + "="*50)
    print("TEST SUMMARY:")
    print(f"Simple tests: {'PASSED' if simple_passed else 'FAILED'}")
    print(f"Pytest: {'PASSED' if pytest_passed else 'FAILED'}")
    
    if simple_passed and pytest_passed:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed!")
        sys.exit(1)