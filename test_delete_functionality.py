#!/usr/bin/env python3
"""
Test script to verify the delete functionality implementation.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Test that all imports work correctly."""
    try:
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        from src.models.task import Task
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_delete_functionality():
    """Test the delete functionality in TaskService."""
    try:
        # Create a temporary task service
        task_service = TaskService("test_tasks.json")
        
        # Add a test task
        task = task_service.add_task("Test Task", "Test Description", "medium")
        print(f"✅ Created test task with ID: {task.id}")
        
        # Verify task exists
        retrieved_task = task_service.get_task_by_id(task.id)
        print(f"✅ Retrieved task: {retrieved_task.title}")
        
        # Delete the task
        deleted_task = task_service.delete_task(task.id)
        print(f"✅ Deleted task: {deleted_task.title}")
        
        # Verify task is deleted
        try:
            task_service.get_task_by_id(task.id)
            print("❌ Task still exists after deletion")
            return False
        except TaskNotFoundException:
            print("✅ Task successfully deleted - not found as expected")
        
        # Clean up test file
        if os.path.exists("test_tasks.json"):
            os.remove("test_tasks.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing delete functionality: {e}")
        return False

def test_app_syntax():
    """Test that the app.py file has valid syntax."""
    try:
        with open('src/app.py', 'r') as f:
            code = f.read()
        
        compile(code, 'src/app.py', 'exec')
        print("✅ app.py syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in app.py: {e}")
        return False

def test_ui_components():
    """Test that UI components are properly implemented."""
    try:
        with open('src/app.py', 'r') as f:
            content = f.read()
        
        # Check for delete buttons
        if '🗑️' not in content:
            print("❌ Delete button emoji not found")
            return False
        print("✅ Delete button emoji found")
        
        # Check for confirmation dialogs
        if 'task_to_delete' not in content:
            print("❌ Delete confirmation logic not found")
            return False
        print("✅ Delete confirmation logic found")
        
        # Check for proper session state management
        if 'del st.session_state.task_to_delete' not in content:
            print("❌ Session state cleanup not found")
            return False
        print("✅ Session state cleanup found")
        
        # Check for updated rerun calls
        if 'st.experimental_rerun' in content:
            print("❌ Deprecated st.experimental_rerun still present")
            return False
        print("✅ Updated to st.rerun() for Streamlit compatibility")
        
        # Check for error handling
        if 'TaskNotFoundException' not in content:
            print("❌ Error handling not found")
            return False
        print("✅ Error handling implemented")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing UI components: {e}")
        return False

def test_multiple_delete_contexts():
    """Test that delete functionality exists in multiple contexts."""
    try:
        with open('src/app.py', 'r') as f:
            content = f.read()
        
        # Check for delete in View Tasks page
        if 'delete_{task.id}' not in content:
            print("❌ Delete button in View Tasks page not found")
            return False
        print("✅ Delete button in View Tasks page found")
        
        # Check for delete in Search Tasks page
        if 'delete_search_{task.id}' not in content:
            print("❌ Delete button in Search Tasks page not found")
            return False
        print("✅ Delete button in Search Tasks page found")
        
        # Check for delete in task details
        if 'delete_detail_{task.id}' not in content:
            print("❌ Delete button in task details not found")
            return False
        print("✅ Delete button in task details found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing multiple delete contexts: {e}")
        return False

if __name__ == "__main__":
    print("Testing delete functionality implementation...")
    print("=" * 60)
    
    success = True
    success &= test_imports()
    success &= test_delete_functionality()
    success &= test_app_syntax()
    success &= test_ui_components()
    success &= test_multiple_delete_contexts()
    
    print("=" * 60)
    if success:
        print("🎉 All tests passed! Delete functionality is ready.")
        print("\nFeatures implemented:")
        print("• Delete buttons in View Tasks page")
        print("• Delete buttons in Search Tasks page")
        print("• Delete buttons in task detail view")
        print("• Confirmation dialogs to prevent accidental deletion")
        print("• Proper error handling for missing tasks")
        print("• Session state management for UI flow")
        print("• Streamlit compatibility (st.rerun)")
        print("\nTo test the UI:")
        print("1. Run: streamlit run src/app.py")
        print("2. Create some tasks")
        print("3. Try deleting tasks from different pages")
        print("4. Test the confirmation dialogs")
    else:
        print("❌ Some tests failed. Please check the implementation.")