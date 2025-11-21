#!/usr/bin/env python3
"""
Demo script to showcase the delete functionality.
This creates sample tasks for demonstration purposes.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.task_service import TaskService


def create_demo_tasks():
    """Create sample tasks for demonstration."""
    print("Creating demo tasks for delete functionality demonstration...")
    
    # Initialize task service with the actual config file
    config_dir = os.path.join(os.path.dirname(__file__), "config")
    os.makedirs(config_dir, exist_ok=True)
    storage_file = os.path.join(config_dir, "tasks.json")
    
    task_service = TaskService(storage_file)
    
    # Clear existing tasks
    existing_tasks = task_service.get_all_tasks()
    print(f"\nFound {len(existing_tasks)} existing tasks. Clearing...")
    for task in existing_tasks:
        task_service.delete_task(task.id)
    
    # Create demo tasks
    demo_tasks = [
        ("Buy groceries", "Get milk, eggs, bread, and vegetables", "high"),
        ("Complete project report", "Finish the Q4 project summary report", "high"),
        ("Call dentist", "Schedule annual checkup appointment", "medium"),
        ("Update resume", "Add recent projects and skills", "medium"),
        ("Read documentation", "Go through the new API documentation", "low"),
        ("Exercise", "30 minutes cardio workout", "medium"),
        ("Pay bills", "Electricity, water, and internet bills", "high"),
        ("Learn Python", "Complete chapter 5 of Python tutorial", "low"),
    ]
    
    print(f"\nCreating {len(demo_tasks)} demo tasks...\n")
    
    created_tasks = []
    for title, description, priority in demo_tasks:
        task = task_service.add_task(title, description, priority)
        created_tasks.append(task)
        print(f"✓ Created: [{priority.upper()}] {title} (ID: {task.id})")
    
    # Mark some tasks as completed
    print("\nMarking some tasks as completed...")
    task_service.complete_task(created_tasks[4].id)  # Read documentation
    task_service.complete_task(created_tasks[7].id)  # Learn Python
    print(f"✓ Marked 2 tasks as completed")
    
    print("\n" + "="*70)
    print("DEMO TASKS CREATED SUCCESSFULLY!")
    print("="*70)
    print("\nTo see the delete functionality in action:")
    print("1. Run: streamlit run src/app.py")
    print("2. Navigate to 'View Tasks' page")
    print("3. Click the 🗑️ button next to any task")
    print("4. Confirm or cancel the deletion")
    print("5. Try deleting from 'Search Tasks' page as well")
    print("\nFeatures to test:")
    print("- Delete button appears next to each task")
    print("- Confirmation dialog shows task title")
    print("- 'Yes, Delete' and 'Cancel' buttons work")
    print("- Deleted tasks disappear from the list")
    print("- Success message appears after deletion")
    print("- Works for both completed and incomplete tasks")
    print("\n" + "="*70)


if __name__ == "__main__":
    create_demo_tasks()
