"""
Tests for UI components and imports.
"""

import pytest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestUIImports:
    """Test that UI components can be imported without errors."""

    def test_streamlit_app_imports(self):
        """Test that the main Streamlit app can be imported."""
        try:
            # Import the main app module
            from src import app
            assert hasattr(app, 'main')
            assert hasattr(app, 'display_tasks_page')
            assert hasattr(app, 'add_task_page')
            assert hasattr(app, 'search_tasks_page')
        except ImportError as e:
            pytest.fail(f"Failed to import Streamlit app: {e}")

    def test_cli_imports(self):
        """Test that the CLI module can be imported."""
        try:
            from src import cli
            assert hasattr(cli, 'main')
        except ImportError as e:
            pytest.fail(f"Failed to import CLI module: {e}")

    def test_all_dependencies_available(self):
        """Test that all required dependencies are available."""
        try:
            import streamlit
            import json
            import os
            import sys
            import tempfile
            import pytest
            from datetime import datetime
            from typing import List, Dict, Any, Optional
        except ImportError as e:
            pytest.fail(f"Missing required dependency: {e}")

    def test_task_service_integration_with_ui_patterns(self):
        """Test that TaskService works with patterns used in UI."""
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        import tempfile
        
        # Create temporary service
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            service = TaskService(temp_file)
            
            # Test patterns used in UI
            # 1. Add task (from Add Task page)
            task = service.add_task("UI Test Task", "Test description", "high")
            assert task.id is not None
            
            # 2. Get all tasks (from View Tasks page)
            all_tasks = service.get_all_tasks(show_completed=True)
            assert len(all_tasks) == 1
            
            # 3. Complete task (from View Tasks page)
            completed_task = service.complete_task(task.id)
            assert completed_task.completed is True
            
            # 4. Search tasks (from Search Tasks page)
            search_results = service.search_tasks("UI Test")
            assert len(search_results) == 1
            
            # 5. Get task by ID (from Search Tasks page detail view)
            retrieved_task = service.get_task_by_id(task.id)
            assert retrieved_task.id == task.id
            
            # 6. Delete task (new functionality)
            deleted_task = service.delete_task(task.id)
            assert deleted_task.id == task.id
            
            # 7. Verify task is gone
            assert len(service.get_all_tasks()) == 0
            
            # 8. Test error handling for UI
            with pytest.raises(TaskNotFoundException):
                service.get_task_by_id(task.id)
            
            with pytest.raises(TaskNotFoundException):
                service.delete_task(999)
                
        finally:
            # Cleanup
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_session_state_patterns(self):
        """Test patterns that would be used with Streamlit session state."""
        from src.services.task_service import TaskService
        import tempfile
        
        # Simulate session state patterns
        session_state = {}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            service = TaskService(temp_file)
            task = service.add_task("Session Test Task")
            
            # Simulate setting confirmation state (like in UI)
            session_state[f"confirm_delete_{task.id}"] = True
            assert session_state.get(f"confirm_delete_{task.id}", False) is True
            
            # Simulate deletion and cleanup
            if session_state.get(f"confirm_delete_{task.id}", False):
                deleted_task = service.delete_task(task.id)
                # Clean up session state
                if f"confirm_delete_{task.id}" in session_state:
                    del session_state[f"confirm_delete_{task.id}"]
            
            assert f"confirm_delete_{task.id}" not in session_state
            assert len(service.get_all_tasks()) == 0
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)