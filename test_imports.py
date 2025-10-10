#!/usr/bin/env python3
"""
Simple script to test that all imports work correctly.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    from src.services.task_service import TaskService
    from src.models.task import Task
    from src.utils.exceptions import TaskNotFoundException
    print("✓ All imports successful")
    
    # Test basic functionality
    service = TaskService("test_tasks.json")
    task = service.add_task("Test Task", "Test Description", "high")
    print(f"✓ Task created: {task}")
    
    # Test delete functionality
    service.delete_task(task.id)
    print("✓ Task deleted successfully")
    
    # Clean up
    if os.path.exists("test_tasks.json"):
        os.remove("test_tasks.json")
    
    print("✓ All basic functionality tests passed")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)