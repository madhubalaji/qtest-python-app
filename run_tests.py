#!/usr/bin/env python3
"""
Test runner script for the task manager application.
"""

import sys
import os
import pytest


# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def run_tests():
    """Run all tests using pytest."""
    print("Running task manager tests...")

    # Import modules to verify they can be loaded
    try:
        from src.services.task_service import TaskService
        from src.utils.exceptions import TaskNotFoundException
        print("✓ All modules imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return 1

    # Run pytest
    test_args = [
        "-v",  # verbose output
        "--tb=short",  # shorter traceback format
        "tests/"  # test directory
    ]

    try:
        exit_code = pytest.main(test_args)
        if exit_code == 0:
            print("✓ All tests passed!")
        else:
            print(f"✗ Tests failed with exit code {exit_code}")
        return exit_code
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        return 1


def run_linting():
    """Run code quality checks."""
    print("Running code quality checks...")

    try:
        import subprocess
        # Run flake8 for syntax errors and undefined names
        result = subprocess.run([
            "flake8", ".",
            "--count",
            "--select=E9,F63,F7,F82",
            "--show-source",
            "--statistics"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("✗ Critical linting errors found:")
            print(result.stdout)
            return result.returncode

        print("✓ No critical linting errors found")
        return 0
    except FileNotFoundError:
        print("⚠ flake8 not found, skipping linting")
        return 0


if __name__ == "__main__":
    print("Task Manager Test Suite")
    print("=" * 50)

    # Run linting first
    lint_result = run_linting()
    if lint_result != 0:
        print("Linting failed, but continuing with tests...")

    # Run tests
    test_result = run_tests()

    print("=" * 50)
    if test_result == 0:
        print("✓ All checks passed!")
    else:
        print("✗ Some checks failed")

    sys.exit(test_result)