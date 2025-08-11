#!/usr/bin/env python3
"""
Script to run tests and check the implementation.
"""

import sys
import os
import subprocess

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

def run_tests():
    """Run the test suite."""
    try:
        # Run pytest
        result = subprocess.run(['python', '-m', 'pytest', 'tests/', '-v'], 
                              capture_output=True, text=True, cwd='/workspace')
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def check_imports():
    """Check if all imports work correctly."""
    try:
        from src.models.task import Task
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

if __name__ == "__main__":
    print("Checking imports...")
    imports_ok = check_imports()
    
    print("\nRunning tests...")
    tests_ok = run_tests()
    
    if imports_ok and tests_ok:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some issues found")