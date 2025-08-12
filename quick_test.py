#!/usr/bin/env python3

import sys
import os
import tempfile

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.services.task_service import TaskService

def test_id_generation():
    """Test the ID generation fix."""
    print("Testing ID generation after deletions...")
    
    # Create temporary storage
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write('[]')
        temp_file = f.name
    
    try:
        service = TaskService(temp_file)
        
        # Add initial tasks (should get IDs 1, 2, 3)
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")
        
        print(f"Initial tasks: {task1.id}, {task2.id}, {task3.id}")
        print(f"Next ID before deletions: {service._next_id}")
        
        # Delete tasks 1 and 3
        service.delete_task(1)
        service.delete_task(3)
        
        print(f"Remaining tasks: {[t.id for t in service.tasks]}")
        print(f"Next ID after deletions: {service._next_id}")
        
        # Add new task (should get ID 4, not 3)
        new_task = service.add_task("New Task")
        
        print(f"New task ID: {new_task.id}")
        
        if new_task.id == 4:
            print("✓ ID generation test PASSED!")
            return True
        else:
            print(f"✗ ID generation test FAILED! Expected 4, got {new_task.id}")
            return False
            
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)

if __name__ == "__main__":
    success = test_id_generation()
    sys.exit(0 if success else 1)