#!/usr/bin/env python3
"""
Demo script to showcase the new delete task functionality.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.services.task_service import TaskService

def demo_delete_feature():
    """Demonstrate the delete task feature."""
    print("🗑️  Task Manager - Delete Feature Demo")
    print("=" * 50)
    
    # Use the actual config file
    config_dir = os.path.join(os.path.dirname(__file__), "config")
    os.makedirs(config_dir, exist_ok=True)
    storage_file = os.path.join(config_dir, "tasks.json")
    
    task_service = TaskService(storage_file)
    
    print("\n📋 Current Tasks:")
    tasks = task_service.get_all_tasks()
    if not tasks:
        print("   No tasks found. Let's add some demo tasks!")
        
        # Add some demo tasks
        task1 = task_service.add_task("Buy groceries", "Milk, bread, eggs", "medium")
        task2 = task_service.add_task("Finish project", "Complete the quarterly report", "high")
        task3 = task_service.add_task("Call dentist", "Schedule appointment", "low")
        task4 = task_service.add_task("Exercise", "Go for a 30-minute run", "medium")
        
        print(f"   ✅ Added demo task: {task1.title}")
        print(f"   ✅ Added demo task: {task2.title}")
        print(f"   ✅ Added demo task: {task3.title}")
        print(f"   ✅ Added demo task: {task4.title}")
        
        tasks = task_service.get_all_tasks()
    
    print(f"\n📊 Total tasks: {len(tasks)}")
    for i, task in enumerate(tasks, 1):
        status = "✓ Completed" if task.completed else "⏳ Active"
        priority_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(task.priority, "⚪")
        print(f"   {i}. [{task.id}] {task.title} - {priority_emoji} {task.priority.upper()} - {status}")
    
    print("\n🗑️  Delete Feature Capabilities:")
    print("   • Delete any task (completed or active)")
    print("   • Confirmation dialog prevents accidental deletion")
    print("   • Available in both 'View Tasks' and 'Search Tasks' pages")
    print("   • Proper error handling for non-existent tasks")
    print("   • Immediate UI feedback and task list refresh")
    
    print("\n🎯 How to use the delete feature:")
    print("   1. Start the Streamlit app: streamlit run src/app.py")
    print("   2. Navigate to 'View Tasks' page")
    print("   3. Click the 🗑️ button next to any task")
    print("   4. Confirm deletion in the warning dialog")
    print("   5. Task will be permanently removed")
    
    print("\n🔍 Delete feature is also available in Search:")
    print("   1. Go to 'Search Tasks' page")
    print("   2. Search for a task and click 'View'")
    print("   3. Click 'Delete Task' button in task details")
    print("   4. Confirm deletion")
    
    print("\n⚠️  Important Notes:")
    print("   • Deletion is permanent and cannot be undone")
    print("   • Deleted tasks are immediately removed from storage")
    print("   • Task IDs are not reused after deletion")
    print("   • All task operations (add, complete, search) work normally with delete feature")
    
    print("\n🧪 Backend API:")
    print("   The TaskService.delete_task(task_id) method:")
    print("   • Returns the deleted Task object")
    print("   • Raises TaskNotFoundException if task doesn't exist")
    print("   • Automatically saves changes to storage")
    
    if tasks:
        print(f"\n💡 Example: To delete the first task ('{tasks[0].title}'):")
        print(f"   task_service.delete_task({tasks[0].id})")
    
    print("\n" + "=" * 50)
    print("🎉 Delete feature is ready to use!")
    print("   Run 'streamlit run src/app.py' to try it out!")

if __name__ == '__main__':
    demo_delete_feature()