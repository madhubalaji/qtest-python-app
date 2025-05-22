"""
Test that the package can be imported.
This is a simple test to verify that the CI/CD workflow is working correctly.
"""

import unittest
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestPackage(unittest.TestCase):
    """Test that the package can be imported."""

    def test_import_src(self):
        """Test that the src package can be imported."""
        import src
        self.assertIsNotNone(src)

    def test_import_models(self):
        """Test that the models module can be imported."""
        import src.models
        self.assertIsNotNone(src.models)

    def test_import_services(self):
        """Test that the services module can be imported."""
        import src.services
        self.assertIsNotNone(src.services)

    def test_import_utils(self):
        """Test that the utils module can be imported."""
        import src.utils
        self.assertIsNotNone(src.utils)


if __name__ == "__main__":
    unittest.main()