"""
Test script to verify all imports work correctly.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def test_imports():
    """Test all critical imports."""
    try:
        from src.services.task_service import TaskService
        print("✓ TaskService import successful")
        
        from src.utils.exceptions import TaskNotFoundException
        print("✓ TaskNotFoundException import successful")
        
        from src.models.task import Task
        print("✓ Task model import successful")
        
        # Test basic functionality
        task = Task(1, "Test Task", "Description", "medium", False)
        print("✓ Task creation successful")
        
        # Test TaskService
        service = TaskService("test_tasks.json")
        print("✓ TaskService creation successful")
        
        print("\nAll imports and basic functionality tests passed!")
        return True

    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False


if __name__ == "__main__":
    test_imports()