#!/usr/bin/env python3
"""
Script to run all tests for the task management application.
"""

import unittest
import sys
import os

if __name__ == "__main__":
    # Add the project root directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Discover and run all tests in the tests directory
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), "tests")
    suite = loader.discover(start_dir)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())