"""
Pytest configuration and shared fixtures.
"""

import pytest
import sys
import os

# Add the project root to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up the test environment before each test."""
    # Ensure we're in a clean state for each test
    pass