#!/usr/bin/env python3
"""
Demo script to showcase the delete functionality implementation.
"""

import sys
import os
import tempfile

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def demo_delete_functionality():
    """Demonstrate the delete functionality."""
    print("🚀 Task Manager Delete Functionality Demo")
    print("=" * 50)
    
    # Create a temporary storage file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        # Initialize the task service
        service = TaskService(temp_file)
        
        print("📝 Creating sample tasks...")
        
        # Add some sample tasks
        task1 = service.add_task("Buy groceries", "Milk, bread, eggs", "high")
        task2 = service.add_task("Write report", "Quarterly sales report", "medium")
        task3 = service.add_task("Call dentist", "Schedule appointment", "low")
        task4 = service.add_task("Exercise", "30 minutes cardio", "medium")
        
        print(f"✅ Created {len(service.get_all_tasks())} tasks")
        
        # Display all tasks
        print("\n📋 Current tasks:")
        for task in service.get_all_tasks():
            status = "✓" if task.completed else "○"
            print(f"  {status} [{task.id}] {task.title} ({task.priority} priority)")
        
        print(f"\n🗑️  Deleting task: '{task2.title}'")
        
        # Delete a task
        deleted_task = service.delete_task(task2.id)
        print(f"✅ Successfully deleted: {deleted_task.title}")
        
        # Show remaining tasks
        print(f"\n📋 Remaining tasks ({len(service.get_all_tasks())} total):")
        for task in service.get_all_tasks():
            status = "✓" if task.completed else "○"
            print(f"  {status} [{task.id}] {task.title} ({task.priority} priority)")
        
        # Try to delete a non-existent task
        print(f"\n🚫 Attempting to delete non-existent task (ID: 999)...")
        try:
            service.delete_task(999)
            print("❌ This should not happen!")
        except TaskNotFoundException as e:
            print(f"✅ Correctly handled error: {e}")
        
        # Complete a task and then delete it
        print(f"\n✓ Completing task: '{task1.title}'")
        service.complete_task(task1.id)
        
        print(f"🗑️  Deleting completed task: '{task1.title}'")
        service.delete_task(task1.id)
        
        # Final state
        print(f"\n📋 Final tasks ({len(service.get_all_tasks())} total):")
        for task in service.get_all_tasks():
            status = "✓" if task.completed else "○"
            print(f"  {status} [{task.id}] {task.title} ({task.priority} priority)")
        
        print("\n🎉 Delete functionality demo completed successfully!")
        
        # Show what's available in the UI
        print("\n🖥️  Frontend Features Added:")
        print("  • Delete button (🗑️) in 'View Tasks' page for each task")
        print("  • Confirmation dialog: 'Are you sure you want to delete [task]?'")
        print("  • Delete option in 'Search Tasks' detail view")
        print("  • Success/error messages after deletion")
        print("  • Automatic page refresh after deletion")
        
        print("\n🔧 Technical Implementation:")
        print("  • Backend: TaskService.delete_task() method (already existed)")
        print("  • Frontend: Added delete buttons with confirmation dialogs")
        print("  • State management: Uses Streamlit session state")
        print("  • Error handling: TaskNotFoundException for missing tasks")
        print("  • Data persistence: Changes saved to JSON file")
        
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)

if __name__ == "__main__":
    demo_delete_functionality()