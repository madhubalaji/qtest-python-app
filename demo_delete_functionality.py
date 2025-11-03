"""
Demo script to showcase the delete functionality in the task manager.
"""

import os
import sys
import tempfile

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.services.task_service import TaskService
from src.models.task import Task

def demo_delete_functionality():
    """Demonstrate the delete functionality."""
    print("=" * 60)
    print("TASK MANAGER - DELETE FUNCTIONALITY DEMO")
    print("=" * 60)
    
    # Create a temporary storage file for the demo
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        # Initialize the task service
        print("\n1. Initializing Task Service...")
        task_service = TaskService(temp_file)
        print("✓ Task service initialized")
        
        # Add some sample tasks
        print("\n2. Adding sample tasks...")
        task1 = task_service.add_task("Complete project documentation", "Write comprehensive docs", "high")
        task2 = task_service.add_task("Review code changes", "Review pull requests", "medium")
        task3 = task_service.add_task("Update dependencies", "Update all package dependencies", "low")
        
        print(f"✓ Added task {task1.id}: {task1.title}")
        print(f"✓ Added task {task2.id}: {task2.title}")
        print(f"✓ Added task {task3.id}: {task3.title}")
        
        # Display all tasks
        print("\n3. Current tasks:")
        tasks = task_service.get_all_tasks()
        for task in tasks:
            status = "Completed" if task.completed else "Active"
            print(f"   ID {task.id}: {task.title} ({status}, {task.priority} priority)")
        
        print(f"\nTotal tasks: {len(tasks)}")
        
        # Complete one task
        print("\n4. Completing a task...")
        completed_task = task_service.complete_task(task2.id)
        print(f"✓ Completed task {completed_task.id}: {completed_task.title}")
        
        # Display tasks again
        print("\n5. Tasks after completion:")
        tasks = task_service.get_all_tasks()
        for task in tasks:
            status = "Completed" if task.completed else "Active"
            print(f"   ID {task.id}: {task.title} ({status}, {task.priority} priority)")
        
        # Demonstrate delete functionality
        print("\n6. Demonstrating DELETE functionality...")
        print(f"   Deleting task {task1.id}: {task1.title}")
        
        try:
            deleted_task = task_service.delete_task(task1.id)
            print(f"✓ Successfully deleted task {deleted_task.id}: {deleted_task.title}")
        except Exception as e:
            print(f"✗ Error deleting task: {e}")
            return False
        
        # Display remaining tasks
        print("\n7. Remaining tasks after deletion:")
        remaining_tasks = task_service.get_all_tasks()
        if remaining_tasks:
            for task in remaining_tasks:
                status = "Completed" if task.completed else "Active"
                print(f"   ID {task.id}: {task.title} ({status}, {task.priority} priority)")
        else:
            print("   No tasks remaining")
        
        print(f"\nTotal remaining tasks: {len(remaining_tasks)}")
        
        # Try to access deleted task (should fail)
        print("\n8. Verifying task deletion...")
        try:
            task_service.get_task_by_id(task1.id)
            print("✗ ERROR: Deleted task is still accessible!")
            return False
        except Exception:
            print(f"✓ Confirmed: Task {task1.id} is no longer accessible (correctly deleted)")
        
        # Delete another task
        print("\n9. Deleting another task...")
        print(f"   Deleting task {task3.id}: {task3.title}")
        
        deleted_task2 = task_service.delete_task(task3.id)
        print(f"✓ Successfully deleted task {deleted_task2.id}: {deleted_task2.title}")
        
        # Final task count
        final_tasks = task_service.get_all_tasks()
        print(f"\n10. Final task count: {len(final_tasks)}")
        
        if len(final_tasks) == 1:
            remaining_task = final_tasks[0]
            print(f"    Only remaining task: ID {remaining_task.id}: {remaining_task.title}")
        
        # Test persistence
        print("\n11. Testing persistence...")
        new_service = TaskService(temp_file)
        persisted_tasks = new_service.get_all_tasks()
        print(f"✓ Persisted tasks after reload: {len(persisted_tasks)}")
        
        if len(persisted_tasks) == len(final_tasks):
            print("✓ Delete operations were properly persisted")
        else:
            print("✗ ERROR: Delete operations were not properly persisted")
            return False
        
        print("\n" + "=" * 60)
        print("DELETE FUNCTIONALITY DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nKey features demonstrated:")
        print("✓ Delete tasks by ID")
        print("✓ Proper error handling for non-existent tasks")
        print("✓ Persistence of delete operations")
        print("✓ Integration with other task operations")
        print("✓ Proper cleanup and task count management")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Demo failed with error: {e}")
        return False
        
    finally:
        # Cleanup temporary file
        if os.path.exists(temp_file):
            os.unlink(temp_file)
            print(f"\n✓ Cleaned up temporary file: {temp_file}")

if __name__ == "__main__":
    success = demo_delete_functionality()
    if not success:
        sys.exit(1)