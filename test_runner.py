"""
Simple test runner for basic functionality testing.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        from src.models.task import Task
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_basic_functionality():
    """Test basic task operations."""
    try:
        from src.models.task import Task
        from src.services.task_service import TaskService
        import tempfile
        import os
        
        # Create temporary storage
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write('[]')
            temp_file = f.name
        
        try:
            # Test TaskService
            service = TaskService(temp_file)
            
            # Test adding tasks
            task1 = service.add_task("Test Task 1", "Description 1", "high")
            task2 = service.add_task("Test Task 2", "Description 2", "medium")
            
            assert task1.id == 1
            assert task2.id == 2
            assert len(service.tasks) == 2
            
            # Test getting tasks
            retrieved_task = service.get_task_by_id(1)
            assert retrieved_task.title == "Test Task 1"
            
            # Test completing task
            completed_task = service.complete_task(1)
            assert completed_task.completed
            
            # Test deleting task
            deleted_task = service.delete_task(2)
            assert deleted_task.id == 2
            assert len(service.tasks) == 1
            
            # Test search
            results = service.search_tasks("Test Task 1")
            assert len(results) == 1
            
            print("✓ Basic functionality tests passed")
            return True
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False


def test_task_model():
    """Test Task model functionality."""
    try:
        from src.models.task import Task
        
        # Test task creation
        task = Task(1, "Test Task", "Test Description", "high", False, "2023-01-01 10:00:00")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert not task.completed
        assert task.created_at == "2023-01-01 10:00:00"
        
        # Test to_dict
        task_dict = task.to_dict()
        expected_dict = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "completed": False,
            "created_at": "2023-01-01 10:00:00"
        }
        assert task_dict == expected_dict
        
        # Test from_dict
        restored_task = Task.from_dict(task_dict)
        assert restored_task.id == task.id
        assert restored_task.title == task.title
        assert restored_task.description == task.description
        assert restored_task.priority == task.priority
        assert restored_task.completed == task.completed
        assert restored_task.created_at == task.created_at
        
        print("✓ Task model tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Task model test failed: {e}")
        return False


if __name__ == "__main__":
    print("Running basic tests...")
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_basic_functionality()
    all_passed &= test_task_model()
    
    if all_passed:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)