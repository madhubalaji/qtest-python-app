"""
Comprehensive test runner for the task manager application.
"""

import os
import sys
import subprocess
import json

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_imports():
    """Test all imports."""
    print("Testing imports...")
    try:
        from src.models.task import Task
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality."""
    print("Testing basic functionality...")
    try:
        from src.models.task import Task
        
        # Test task creation
        task = Task(1, "Test Task", "Description", "medium", False)
        assert task.id == 1
        assert task.title == "Test Task"
        
        # Test task serialization
        task_dict = task.to_dict()
        assert task_dict["id"] == 1
        
        # Test task deserialization
        new_task = Task.from_dict(task_dict)
        assert new_task.id == task.id
        
        print("✓ Basic functionality tests passed")
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_service_functionality():
    """Test service functionality."""
    print("Testing service functionality...")
    try:
        import tempfile
        from src.services.task_service import TaskService
        
        # Create temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            service = TaskService(temp_file)
            
            # Test adding task
            task = service.add_task("Test Task", "Description", "high")
            assert task.id == 1
            
            # Test getting task
            retrieved = service.get_task_by_id(task.id)
            assert retrieved.title == "Test Task"
            
            # Test updating task
            updated = service.update_task(task.id, title="Updated Task")
            assert updated.title == "Updated Task"
            
            # Test completing task
            completed = service.complete_task(task.id)
            assert completed.completed is True
            
            # Test deleting task
            deleted = service.delete_task(task.id)
            assert deleted.id == task.id
            assert len(service.tasks) == 0
            
            print("✓ Service functionality tests passed")
            return True
            
        finally:
            # Cleanup
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        print(f"✗ Service functionality test failed: {e}")
        return False

def test_ui_imports():
    """Test UI-related imports."""
    print("Testing UI imports...")
    try:
        import streamlit
        print("✓ Streamlit import successful")
        
        import src.app
        print("✓ App module import successful")
        
        import src.cli
        print("✓ CLI module import successful")
        
        return True
    except Exception as e:
        print(f"✗ UI import test failed: {e}")
        return False

def run_pytest():
    """Run pytest tests."""
    print("Running pytest tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "-v", 
            "--tb=short",
            "tests/"
        ], capture_output=True, text=True)
        
        print("Pytest output:")
        print(result.stdout)
        
        if result.stderr:
            print("Pytest errors:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Pytest execution failed: {e}")
        return False

def run_flake8():
    """Run flake8 style checks."""
    print("Running flake8 style checks...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "flake8", 
            "--count", 
            "--select=E9,F63,F7,F82", 
            "--show-source", 
            "--statistics",
            "."
        ], capture_output=True, text=True)
        
        if result.stdout:
            print("Flake8 critical errors:")
            print(result.stdout)
        
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Flake8 execution failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("TASK MANAGER - COMPREHENSIVE TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Basic Functionality Tests", test_basic_functionality),
        ("Service Functionality Tests", test_service_functionality),
        ("UI Import Tests", test_ui_imports),
        ("Pytest Tests", run_pytest),
        ("Style Checks", run_flake8)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'-' * 30}")
        print(f"Running: {test_name}")
        print(f"{'-' * 30}")
        
        success = test_func()
        results.append((test_name, success))
        
        if success:
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print(f"\n{'=' * 50}")
    print("TEST SUMMARY")
    print(f"{'=' * 50}")
    
    passed = 0
    for test_name, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nTotal: {len(results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {len(results) - passed}")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"\n❌ {len(results) - passed} TESTS FAILED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)