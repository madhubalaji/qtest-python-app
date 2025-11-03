"""
Tests for UI imports and basic functionality.
"""

import os
import sys
import pytest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestUIImports:
    """Test UI-related imports and basic functionality."""

    def test_streamlit_import(self):
        """Test that streamlit can be imported."""
        try:
            import streamlit as st
            assert True
        except ImportError:
            pytest.fail("Streamlit import failed")

    def test_app_module_import(self):
        """Test that the app module can be imported."""
        try:
            import src.app
            assert hasattr(src.app, 'main')
            assert hasattr(src.app, 'display_tasks_page')
            assert hasattr(src.app, 'add_task_page')
            assert hasattr(src.app, 'search_tasks_page')
        except ImportError as e:
            pytest.fail(f"App module import failed: {e}")

    def test_cli_module_import(self):
        """Test that the CLI module can be imported."""
        try:
            import src.cli
            assert hasattr(src.cli, 'main')
        except ImportError as e:
            pytest.fail(f"CLI module import failed: {e}")

    def test_task_service_import(self):
        """Test that TaskService can be imported."""
        try:
            from src.services.task_service import TaskService
            assert TaskService is not None
        except ImportError as e:
            pytest.fail(f"TaskService import failed: {e}")

    def test_task_model_import(self):
        """Test that Task model can be imported."""
        try:
            from src.models.task import Task
            assert Task is not None
        except ImportError as e:
            pytest.fail(f"Task model import failed: {e}")

    def test_exceptions_import(self):
        """Test that exceptions can be imported."""
        try:
            from src.utils.exceptions import TaskNotFoundException
            assert TaskNotFoundException is not None
        except ImportError as e:
            pytest.fail(f"Exceptions import failed: {e}")

    def test_task_service_functionality(self, task_service):
        """Test basic TaskService functionality for UI integration."""
        # Test adding a task
        task = task_service.add_task("UI Test Task", "Test description", "high")
        assert task.id == 1
        assert task.title == "UI Test Task"

        # Test getting all tasks
        tasks = task_service.get_all_tasks()
        assert len(tasks) == 1

        # Test completing a task
        completed_task = task_service.complete_task(task.id)
        assert completed_task.completed is True

        # Test deleting a task
        deleted_task = task_service.delete_task(task.id)
        assert deleted_task.id == task.id
        assert len(task_service.tasks) == 0

    def test_task_model_functionality(self):
        """Test basic Task model functionality for UI integration."""
        from src.models.task import Task
        
        # Test task creation
        task = Task(1, "UI Test Task", "Test description", "high", False)
        assert task.id == 1
        assert task.title == "UI Test Task"
        assert task.description == "Test description"
        assert task.priority == "high"
        assert task.completed is False

        # Test to_dict conversion
        task_dict = task.to_dict()
        assert task_dict["id"] == 1
        assert task_dict["title"] == "UI Test Task"

        # Test from_dict creation
        new_task = Task.from_dict(task_dict)
        assert new_task.id == task.id
        assert new_task.title == task.title