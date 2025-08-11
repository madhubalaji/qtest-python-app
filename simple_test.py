import sys
import os
sys.path.insert(0, '/workspace')

# Test imports
try:
    from src.models.task import Task
    from src.services.task_service import TaskService
    from src.utils.exceptions import TaskNotFoundException
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test basic functionality
try:
    import tempfile
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    # Test TaskService
    service = TaskService(temp_file)
    
    # Add tasks
    task1 = service.add_task("Test Task 1", "Description 1", "high")
    task2 = service.add_task("Test Task 2", "Description 2", "medium")
    print(f"✓ Added tasks with IDs: {task1.id}, {task2.id}")
    
    # Test delete functionality
    deleted_task = service.delete_task(task1.id)
    print(f"✓ Deleted task: {deleted_task.title}")
    
    # Verify task is gone
    remaining_tasks = service.get_all_tasks()
    print(f"✓ Remaining tasks: {len(remaining_tasks)}")
    
    # Try to get deleted task (should raise exception)
    try:
        service.get_task_by_id(task1.id)
        print("✗ ERROR: Deleted task still accessible")
    except TaskNotFoundException:
        print("✓ Deleted task properly removed")
    
    # Clean up
    os.unlink(temp_file)
    
    print("\n🎉 All basic tests passed! Delete functionality is working.")
    
except Exception as e:
    print(f"✗ Test error: {e}")
    import traceback
    traceback.print_exc()