#!/usr/bin/env python3
"""
Simple script to test that all imports work correctly.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_imports():
    """Test all critical imports."""
    try:
        print("Testing imports...")
        
        # Test model imports
        from src.models.task import Task
        print("✓ Task model imported successfully")
        
        # Test service imports
        from src.services.task_service import TaskService
        print("✓ TaskService imported successfully")
        
        # Test exception imports
        from src.utils.exceptions import TaskNotFoundException, TaskManagerException
        print("✓ Exceptions imported successfully")
        
        # Test basic functionality
        task = Task(1, "Test Task")
        print(f"✓ Task creation works: {task}")
        
        service = TaskService("test_tasks.json")
        print("✓ TaskService creation works")
        
        # Clean up test file if created
        if os.path.exists("test_tasks.json"):
            os.remove("test_tasks.json")
        
        print("\n🎉 All imports and basic functionality work correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)