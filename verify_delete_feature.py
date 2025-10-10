#!/usr/bin/env python3
"""
Quick verification that the delete feature implementation is working.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def verify_implementation():
    """Verify the delete functionality implementation."""
    print("🔍 Verifying Delete Task Implementation")
    print("=" * 40)
    
    # Test 1: Check imports
    print("\n1. Testing imports...")
    try:
        from src.services.task_service import TaskService
        from src.models.task import Task
        from src.utils.exceptions import TaskNotFoundException
        print("   ✅ All imports successful")
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test 2: Check TaskService has delete method
    print("\n2. Checking TaskService delete method...")
    try:
        # Check if delete_task method exists
        if hasattr(TaskService, 'delete_task'):
            print("   ✅ delete_task method exists")
        else:
            print("   ❌ delete_task method not found")
            return False
    except Exception as e:
        print(f"   ❌ Error checking method: {e}")
        return False
    
    # Test 3: Check app.py syntax
    print("\n3. Checking app.py syntax...")
    try:
        with open('src/app.py', 'r') as f:
            code = f.read()
        compile(code, 'src/app.py', 'exec')
        print("   ✅ app.py syntax is valid")
    except SyntaxError as e:
        print(f"   ❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 4: Check for delete button code in app.py
    print("\n4. Checking for delete functionality in UI...")
    try:
        with open('src/app.py', 'r') as f:
            content = f.read()
        
        checks = [
            ('Delete button emoji', '🗑️' in content),
            ('Delete confirmation', 'confirm_delete_' in content),
            ('Delete task call', 'delete_task(' in content),
            ('TaskNotFoundException handling', 'TaskNotFoundException' in content),
        ]
        
        all_passed = True
        for check_name, result in checks:
            if result:
                print(f"   ✅ {check_name} found")
            else:
                print(f"   ❌ {check_name} not found")
                all_passed = False
        
        if not all_passed:
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking UI code: {e}")
        return False
    
    # Test 5: Quick functional test
    print("\n5. Testing delete functionality...")
    try:
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            task_service = TaskService(temp_file)
            
            # Add a task
            task = task_service.add_task("Test Task", "Test Description", "medium")
            task_id = task.id
            
            # Verify task exists
            all_tasks_before = task_service.get_all_tasks()
            if len(all_tasks_before) != 1:
                print(f"   ❌ Expected 1 task, got {len(all_tasks_before)}")
                return False
            
            # Delete the task
            deleted_task = task_service.delete_task(task_id)
            
            # Verify task was deleted
            all_tasks_after = task_service.get_all_tasks()
            if len(all_tasks_after) != 0:
                print(f"   ❌ Expected 0 tasks after deletion, got {len(all_tasks_after)}")
                return False
            
            # Verify deleted task details
            if deleted_task.title != "Test Task":
                print(f"   ❌ Deleted task title mismatch")
                return False
            
            print("   ✅ Delete functionality works correctly")
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        print(f"   ❌ Functional test failed: {e}")
        return False
    
    print("\n🎉 All verification tests passed!")
    print("\nThe delete task functionality has been successfully implemented!")
    return True

def show_usage_instructions():
    """Show how to use the new delete functionality."""
    print("\n" + "=" * 50)
    print("📖 HOW TO USE THE DELETE FUNCTIONALITY")
    print("=" * 50)
    print("\n1. Start the application:")
    print("   streamlit run src/app.py")
    print("\n2. Delete from 'View Tasks' page:")
    print("   • Go to 'View Tasks' in sidebar")
    print("   • Click 🗑️ button next to any task")
    print("   • Confirm deletion in the dialog")
    print("\n3. Delete from 'Search Tasks' page:")
    print("   • Go to 'Search Tasks' in sidebar")
    print("   • Search for tasks")
    print("   • Click 🗑️ in results OR")
    print("   • Click 'View' then 'Delete Task'")
    print("   • Confirm deletion in the dialog")
    print("\n4. Safety features:")
    print("   • Confirmation dialogs prevent accidents")
    print("   • Cancel option available")
    print("   • Error messages for invalid operations")
    print("   • Success messages confirm deletion")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    success = verify_implementation()
    
    if success:
        show_usage_instructions()
        print("\n✅ Implementation verification completed successfully!")
    else:
        print("\n❌ Implementation verification failed!")
        print("Please check the error messages above.")
    
    sys.exit(0 if success else 1)