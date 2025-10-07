#!/usr/bin/env python3
"""
Simple script to test imports before running full test suite.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    from src.services.task_service import TaskService
    print("✓ TaskService import successful")
except ImportError as e:
    print(f"✗ TaskService import failed: {e}")

try:
    from src.models.task import Task
    print("✓ Task model import successful")
except ImportError as e:
    print(f"✗ Task model import failed: {e}")

try:
    from src.utils.exceptions import TaskNotFoundException
    print("✓ Exceptions import successful")
except ImportError as e:
    print(f"✗ Exceptions import failed: {e}")

# Test basic functionality
try:
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()
    
    task_service = TaskService(temp_file.name)
    task = task_service.add_task("Test Task", "Test Description", "high")
    print(f"✓ Task creation successful: {task}")
    
    # Test delete functionality
    deleted_task = task_service.delete_task(task.id)
    print(f"✓ Task deletion successful: {deleted_task}")
    
    # Cleanup
    os.unlink(temp_file.name)
    print("✓ All basic functionality tests passed")
    
except Exception as e:
    print(f"✗ Basic functionality test failed: {e}")