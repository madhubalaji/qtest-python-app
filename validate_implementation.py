#!/usr/bin/env python3
"""
Validation script to verify the delete task implementation is complete and functional.
"""

import os
import sys
import ast
import re

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def validate_app_py_changes():
    """Validate that app.py has the required delete functionality."""
    print("🔍 Validating app.py changes...")
    
    with open('/workspace/src/app.py', 'r') as f:
        content = f.read()
    
    # Check for delete buttons in View Tasks page
    delete_button_pattern = r'st\.button\("🗑️".*key=f"delete_\{task\.id\}"'
    if not re.search(delete_button_pattern, content):
        print("❌ Delete button not found in View Tasks page")
        return False
    print("✅ Delete button found in View Tasks page")
    
    # Check for confirmation dialog
    if 'task_to_delete' not in content:
        print("❌ Delete confirmation logic not found")
        return False
    print("✅ Delete confirmation logic found")
    
    # Check for search page delete functionality
    if 'task_to_delete_search' not in content:
        print("❌ Search page delete functionality not found")
        return False
    print("✅ Search page delete functionality found")
    
    # Check for proper session state cleanup
    if 'del st.session_state.task_to_delete' not in content:
        print("❌ Session state cleanup not found")
        return False
    print("✅ Session state cleanup found")
    
    return True


def validate_task_service():
    """Validate that TaskService has delete_task method."""
    print("\n🔍 Validating TaskService delete functionality...")
    
    try:
        from src.services.task_service import TaskService
        
        # Check if delete_task method exists
        if not hasattr(TaskService, 'delete_task'):
            print("❌ delete_task method not found in TaskService")
            return False
        print("✅ delete_task method found in TaskService")
        
        # Check method signature
        import inspect
        sig = inspect.signature(TaskService.delete_task)
        if 'task_id' not in sig.parameters:
            print("❌ delete_task method doesn't have task_id parameter")
            return False
        print("✅ delete_task method has correct signature")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import TaskService: {e}")
        return False


def validate_ui_structure():
    """Validate the UI structure changes."""
    print("\n🔍 Validating UI structure...")
    
    with open('/workspace/src/app.py', 'r') as f:
        content = f.read()
    
    # Check for 4-column layout in display_tasks_page
    if 'col1, col2, col3, col4 = st.columns([3, 1, 1, 1])' not in content:
        print("❌ 4-column layout not found in display_tasks_page")
        return False
    print("✅ 4-column layout found in display_tasks_page")
    
    # Check for 3-column layout in search results
    search_columns_pattern = r'col1, col2, col3 = st\.columns\(\[3, 1, 1\]\)'
    if not re.search(search_columns_pattern, content):
        print("❌ 3-column layout not found in search results")
        return False
    print("✅ 3-column layout found in search results")
    
    return True


def validate_error_handling():
    """Validate error handling implementation."""
    print("\n🔍 Validating error handling...")
    
    with open('/workspace/src/app.py', 'r') as f:
        content = f.read()
    
    # Check for TaskNotFoundException handling
    if 'except TaskNotFoundException:' not in content:
        print("❌ TaskNotFoundException handling not found")
        return False
    print("✅ TaskNotFoundException handling found")
    
    # Check for error messages
    if 'st.error("Task not found")' not in content:
        print("❌ Error message display not found")
        return False
    print("✅ Error message display found")
    
    return True


def validate_readme_update():
    """Validate README.md was updated."""
    print("\n🔍 Validating README.md update...")
    
    with open('/workspace/README.md', 'r') as f:
        content = f.read()
    
    if 'Delete tasks with confirmation' not in content:
        print("❌ README.md not updated with delete feature")
        return False
    print("✅ README.md updated with delete feature")
    
    return True


def main():
    """Run all validation checks."""
    print("🚀 Starting implementation validation...\n")
    
    checks = [
        ("App.py Changes", validate_app_py_changes),
        ("TaskService", validate_task_service),
        ("UI Structure", validate_ui_structure),
        ("Error Handling", validate_error_handling),
        ("README Update", validate_readme_update),
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        try:
            if check_func():
                passed += 1
            else:
                print(f"❌ {check_name} validation failed")
        except Exception as e:
            print(f"❌ {check_name} validation error: {e}")
    
    print(f"\n📊 Validation Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All validations passed! Delete task functionality is properly implemented.")
        return True
    else:
        print("⚠️  Some validations failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)