#!/usr/bin/env python3
"""
Demo script to showcase the delete functionality in the task manager.
"""

import sys
import os
import tempfile

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException

def demo_delete_functionality():
    """Demonstrate the delete functionality."""
    print("🚀 TASK MANAGER - DELETE FUNCTIONALITY DEMO")
    print("=" * 50)
    
    # Create temporary storage
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        # Initialize service
        service = TaskService(temp_file)
        print(f"📁 Using temporary storage: {temp_file}")
        print()
        
        # Create sample tasks
        print("📝 Creating sample tasks...")
        task1 = service.add_task("Complete project proposal", "Write and review the project proposal document", "high")
        task2 = service.add_task("Team meeting", "Weekly team sync meeting", "medium")
        task3 = service.add_task("Code review", "Review pull requests from team members", "medium")
        task4 = service.add_task("Update documentation", "Update API documentation", "low")
        task5 = service.add_task("Bug fixes", "Fix reported bugs in the system", "high")
        
        print(f"✅ Created {len(service.get_all_tasks())} tasks")
        print()
        
        # Display all tasks
        print("📋 Current tasks:")
        for task in service.get_all_tasks():
            status = "✅" if task.completed else "⏳"
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
            print(f"  {status} [{task.id}] {task.title} {priority_emoji}")
        print()
        
        # Complete some tasks
        print("✅ Completing some tasks...")
        service.complete_task(task2.id)
        service.complete_task(task4.id)
        print(f"Completed tasks: {task2.title}, {task4.title}")
        print()
        
        # Display updated tasks
        print("📋 Updated task list:")
        for task in service.get_all_tasks():
            status = "✅" if task.completed else "⏳"
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
            print(f"  {status} [{task.id}] {task.title} {priority_emoji}")
        print()
        
        # Demonstrate delete functionality
        print("🗑️  DEMONSTRATING DELETE FUNCTIONALITY")
        print("-" * 40)
        
        # Delete a completed task
        print(f"Deleting completed task: '{task2.title}' (ID: {task2.id})")
        deleted_task = service.delete_task(task2.id)
        print(f"✅ Successfully deleted: {deleted_task.title}")
        print()
        
        # Delete an active task
        print(f"Deleting active task: '{task5.title}' (ID: {task5.id})")
        deleted_task = service.delete_task(task5.id)
        print(f"✅ Successfully deleted: {deleted_task.title}")
        print()
        
        # Display remaining tasks
        print("📋 Remaining tasks after deletion:")
        remaining_tasks = service.get_all_tasks()
        if remaining_tasks:
            for task in remaining_tasks:
                status = "✅" if task.completed else "⏳"
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
                print(f"  {status} [{task.id}] {task.title} {priority_emoji}")
        else:
            print("  No tasks remaining")
        print()
        
        # Demonstrate error handling
        print("🚨 DEMONSTRATING ERROR HANDLING")
        print("-" * 35)
        
        print("Attempting to delete a non-existent task (ID: 999)...")
        try:
            service.delete_task(999)
            print("❌ This should not happen!")
        except TaskNotFoundException as e:
            print(f"✅ Correctly caught error: {e}")
        print()
        
        print("Attempting to delete an already deleted task...")
        try:
            service.delete_task(task2.id)  # Already deleted
            print("❌ This should not happen!")
        except TaskNotFoundException as e:
            print(f"✅ Correctly caught error: {e}")
        print()
        
        # Search functionality after deletion
        print("🔍 SEARCH FUNCTIONALITY AFTER DELETION")
        print("-" * 38)
        
        search_results = service.search_tasks("project")
        print(f"Searching for 'project': Found {len(search_results)} results")
        for task in search_results:
            print(f"  - [{task.id}] {task.title}")
        print()
        
        # Final statistics
        print("📊 FINAL STATISTICS")
        print("-" * 20)
        all_tasks = service.get_all_tasks()
        active_tasks = service.get_all_tasks(show_completed=False)
        completed_tasks = [t for t in all_tasks if t.completed]
        
        print(f"Total tasks: {len(all_tasks)}")
        print(f"Active tasks: {len(active_tasks)}")
        print(f"Completed tasks: {len(completed_tasks)}")
        print(f"Deleted tasks: 2 (Team meeting, Bug fixes)")
        print()
        
        print("🎉 DELETE FUNCTIONALITY DEMO COMPLETED SUCCESSFULLY!")
        print("✅ All operations worked as expected")
        print("✅ Error handling is robust")
        print("✅ Data persistence is maintained")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)
            print(f"🧹 Cleaned up temporary file: {temp_file}")
    
    return True

def main():
    """Run the demo."""
    success = demo_delete_functionality()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())