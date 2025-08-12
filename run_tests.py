#!/usr/bin/env python3
"""
Simple test runner script to validate the test suite locally.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and return the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Return code: {e.returncode}")
        if e.stdout:
            print("STDOUT:")
            print(e.stdout)
        if e.stderr:
            print("STDERR:")
            print(e.stderr)
        return False


def main():
    """Main function to run all tests and checks."""
    print("Task Manager - Test Runner")
    print("=" * 60)
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    success_count = 0
    total_tests = 0
    
    # Test commands to run
    test_commands = [
        ("python -m pytest tests/ -v", "Unit Tests"),
        ("python -m pytest tests/ --cov=src --cov-report=term-missing", "Coverage Report"),
        ("python -c 'from src.models.task import Task; print(\"✅ Task model imports successfully\")'", "Task Model Import"),
        ("python -c 'from src.services.task_service import TaskService; print(\"✅ TaskService imports successfully\")'", "TaskService Import"),
        ("python -c 'from src.utils.exceptions import TaskNotFoundException; print(\"✅ Exceptions import successfully\")'", "Exceptions Import"),
        ("python -c 'import src.app; print(\"✅ Streamlit app imports successfully\")'", "Streamlit App Import"),
        ("flake8 src/ --count --statistics", "Code Style Check"),
    ]
    
    for command, description in test_commands:
        total_tests += 1
        if run_command(command, description):
            success_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Passed: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {total_tests - success_count} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())