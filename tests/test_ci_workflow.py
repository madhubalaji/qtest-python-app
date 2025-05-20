"""
Test file to verify that the CI workflow is working correctly.
This file contains basic tests that should always pass.
"""

import os
import sys
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCIWorkflow(unittest.TestCase):
    """Test cases to verify CI workflow."""

    def test_python_version(self):
        """Test that Python version is compatible."""
        import platform
        version = platform.python_version_tuple()
        # Check that Python version is at least 3.6
        self.assertGreaterEqual(int(version[0]), 3)
        if int(version[0]) == 3:
            self.assertGreaterEqual(int(version[1]), 6)

    def test_project_structure(self):
        """Test that the project structure is correct."""
        # Check that essential directories exist
        self.assertTrue(os.path.isdir(os.path.join(os.path.dirname(__file__), '..', 'src')))
        self.assertTrue(os.path.isdir(os.path.join(os.path.dirname(__file__), '..', 'config')))
        
        # Check that essential files exist
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(__file__), '..', 'setup.py')))
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')))

    def test_imports(self):
        """Test that essential modules can be imported."""
        try:
            from src.models.task import Task
            from src.services.task_service import TaskService
            # If we get here, the imports worked
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")


if __name__ == "__main__":
    unittest.main()