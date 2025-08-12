#!/usr/bin/env python3
"""
Test script to verify imports work correctly.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    from src.models.task import Task
    print("✓ Task model imported successfully")
    
    from src.services.task_service import TaskService
    print("✓ TaskService imported successfully")
    
    from src.utils.exceptions import TaskNotFoundException
    print("✓ TaskNotFoundException imported successfully")
    
    # Test basic functionality
    task = Task(1, "Test Task", "Test Description", "medium")
    print(f"✓ Task created: {task}")
    
    # Test task serialization
    task_dict = task.to_dict()
    restored_task = Task.from_dict(task_dict)
    print(f"✓ Task serialization works: {restored_task}")
    
    print("\n✅ All imports and basic functionality work correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)