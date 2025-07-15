#!/usr/bin/env python3
"""
Script to run all tests for the task manager application.
"""

import os
import sys
import unittest
import pytest


def run_tests():
    """Run all tests using unittest and pytest."""
    print("=" * 70)
    print("Running unittest tests...")
    print("=" * 70)
    
    # Discover and run all tests using unittest
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
    
    print("\n" + "=" * 70)
    print("Running pytest tests...")
    print("=" * 70)
    
    # Run all tests using pytest
    pytest.main(['-v', 'tests'])


if __name__ == "__main__":
    # Add the project root directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    run_tests()