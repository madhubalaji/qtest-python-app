"""
Simple test script for quick verification.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from src.models.task import Task
    from src.services.task_service import TaskService
    from src.utils.exceptions import TaskNotFoundException
    
    print("Testing Task Manager Components...")
    
    # Test Task creation
    task = Task(1, "Sample Task", "Sample Description", "high")
    print(f"Created task: {task}")
    
    # Test Task serialization
    task_dict = task.to_dict()
    restored_task = Task.from_dict(task_dict)
    print(f"Serialization test: {restored_task}")
    
    # Test TaskService with temporary storage
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write('[]')
        temp_file = f.name
    
    try:
        service = TaskService(temp_file)
        
        # Add tasks
        task1 = service.add_task("Task 1", "Description 1")
        task2 = service.add_task("Task 2", "Description 2")
        print(f"Added tasks: {task1.id}, {task2.id}")
        
        # Delete task
        deleted = service.delete_task(task1.id)
        print(f"Deleted task: {deleted.id}")
        
        # Add new task after deletion
        task3 = service.add_task("Task 3", "Description 3")
        print(f"New task after deletion: {task3.id}")
        
        print("✓ All basic tests passed!")
        
    finally:
        os.unlink(temp_file)
        
except Exception as e:
    print(f"✗ Test failed: {e}")
    sys.exit(1)