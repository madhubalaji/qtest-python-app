#!/usr/bin/env python3
"""
Test runner script for the task manager application.
This script runs all tests and provides a summary of the CI/CD implementation.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and return the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False


def main():
    """Main function to run all tests and checks."""
    print("Task Manager CI/CD Implementation Test Runner")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('src') or not os.path.exists('tests'):
        print("Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # List of commands to run
    commands = [
        ("python -m pytest tests/ -v", "Running Unit Tests"),
        ("python -m pytest tests/ --cov=src --cov-report=term-missing", "Running Tests with Coverage"),
        ("python -m flake8 . --count --statistics", "Running Linting (flake8)"),
        ("python -m black --check --diff .", "Checking Code Formatting (black)"),
    ]
    
    results = []
    
    for command, description in commands:
        success = run_command(command, description)
        results.append((description, success))
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY OF CI/CD IMPLEMENTATION")
    print('='*60)
    
    print("\n✅ IMPLEMENTED FEATURES:")
    features = [
        "Comprehensive test suite with 4 test modules",
        "Unit tests for Task model, TaskService, exceptions, and CLI",
        "Integration tests for full application workflow",
        "GitHub Actions workflow with multi-platform testing",
        "Support for Python 3.8-3.12 across Ubuntu, Windows, macOS",
        "Code coverage reporting with 85% minimum threshold",
        "Code formatting with Black",
        "Linting with flake8",
        "Build and package verification",
        "Dependency caching for faster builds",
        "Codecov integration for coverage tracking",
        "Development tools (Makefile, configuration files)",
        "Comprehensive documentation updates"
    ]
    
    for feature in features:
        print(f"  • {feature}")
    
    print(f"\n📁 FILES CREATED/MODIFIED:")
    files = [
        "tests/__init__.py - Test package initialization",
        "tests/test_task_model.py - Task model unit tests",
        "tests/test_task_service.py - TaskService unit tests", 
        "tests/test_exceptions.py - Exception handling tests",
        "tests/test_cli.py - CLI interface tests",
        "tests/test_integration.py - Integration tests",
        ".github/workflows/python-app.yml - Enhanced CI/CD workflow",
        "pytest.ini - Pytest configuration",
        ".coveragerc - Coverage configuration",
        ".flake8 - Linting configuration",
        "pyproject.toml - Modern Python project configuration",
        ".gitignore - Git ignore patterns",
        "Makefile - Development task automation",
        "requirements.txt - Updated with testing dependencies",
        "README.md - Enhanced with CI/CD documentation"
    ]
    
    for file in files:
        print(f"  • {file}")
    
    print(f"\n🔧 TEST RESULTS:")
    all_passed = True
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  • {description}: {status}")
        if not success:
            all_passed = False
    
    print(f"\n🚀 CI/CD WORKFLOW FEATURES:")
    workflow_features = [
        "Triggers on push to main/develop branches",
        "Triggers on pull requests",
        "Matrix testing across multiple OS and Python versions",
        "Dependency caching for performance",
        "Parallel test execution",
        "Code quality gates (linting, formatting, coverage)",
        "Build artifact generation and validation",
        "Coverage reporting to Codecov",
        "Fail-fast disabled for comprehensive testing"
    ]
    
    for feature in workflow_features:
        print(f"  • {feature}")
    
    print(f"\n📊 COVERAGE AND QUALITY:")
    quality_features = [
        "Minimum 85% test coverage requirement",
        "Comprehensive unit test coverage for all modules",
        "Integration tests for end-to-end workflows",
        "Code formatting enforced with Black",
        "Linting with flake8 for code quality",
        "Exception handling and error path testing",
        "Parameterized tests for multiple scenarios",
        "Mock testing for external dependencies"
    ]
    
    for feature in quality_features:
        print(f"  • {feature}")
    
    if all_passed:
        print(f"\n🎉 ALL CHECKS PASSED! The CI/CD workflow is ready for use.")
        print("   You can now push changes and the workflow will automatically:")
        print("   - Run tests on multiple platforms and Python versions")
        print("   - Check code quality and formatting")
        print("   - Generate coverage reports")
        print("   - Build and validate the package")
    else:
        print(f"\n⚠️  Some checks failed. Please review the output above.")
        print("   The CI/CD infrastructure is in place, but you may need to:")
        print("   - Install missing dependencies")
        print("   - Fix code formatting issues")
        print("   - Address any failing tests")
    
    print(f"\n{'='*60}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())