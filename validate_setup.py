#!/usr/bin/env python3
"""
Validation script to check that the project setup is correct.
This script validates the CI/CD setup, test configuration, and package structure.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists and report the result."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (NOT FOUND)")
        return False


def check_directory_exists(dirpath, description):
    """Check if a directory exists and report the result."""
    if os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description}: {dirpath} (NOT FOUND)")
        return False


def run_command(command, description):
    """Run a command and report the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        if result.returncode == 0:
            print(f"✅ {description}: PASSED")
            return True
        else:
            print(f"❌ {description}: FAILED")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ {description}: TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {description}: ERROR - {e}")
        return False


def validate_github_workflow():
    """Validate the GitHub Actions workflow file."""
    print("\n🔍 Validating GitHub Actions Workflow...")
    
    workflow_file = ".github/workflows/python-app.yml"
    if not check_file_exists(workflow_file, "GitHub Actions workflow"):
        return False
    
    # Check if workflow uses updated actions
    with open(workflow_file, 'r') as f:
        content = f.read()
        
    checks = [
        ("actions/checkout@v4", "Updated checkout action"),
        ("actions/setup-python@v5", "Updated setup-python action"),
        ("actions/upload-artifact@v4", "Updated upload-artifact action"),
        ("github/codeql-action", "CodeQL security analysis"),
        ("matrix:", "Matrix testing configuration"),
    ]
    
    all_passed = True
    for check, description in checks:
        if check in content:
            print(f"✅ {description}: Found")
        else:
            print(f"❌ {description}: Not found")
            all_passed = False
    
    return all_passed


def validate_test_structure():
    """Validate the test structure and configuration."""
    print("\n🧪 Validating Test Structure...")
    
    test_files = [
        ("tests/__init__.py", "Test package init"),
        ("tests/test_task_model.py", "Task model tests"),
        ("tests/test_task_service.py", "Task service tests"),
        ("tests/test_cli.py", "CLI tests"),
        ("tests/test_exceptions.py", "Exception tests"),
        ("pytest.ini", "Pytest configuration"),
    ]
    
    all_passed = True
    for filepath, description in test_files:
        if not check_file_exists(filepath, description):
            all_passed = False
    
    return all_passed


def validate_package_structure():
    """Validate the package structure."""
    print("\n📦 Validating Package Structure...")
    
    structure_items = [
        ("src/__init__.py", "Source package init"),
        ("src/models/__init__.py", "Models package init"),
        ("src/services/__init__.py", "Services package init"),
        ("src/utils/__init__.py", "Utils package init"),
        ("pyproject.toml", "Project configuration"),
        ("requirements.txt", "Requirements file"),
        ("setup.py", "Setup script"),
    ]
    
    all_passed = True
    for filepath, description in structure_items:
        if not check_file_exists(filepath, description):
            all_passed = False
    
    return all_passed


def validate_dependencies():
    """Validate that required dependencies are listed."""
    print("\n📋 Validating Dependencies...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    with open("requirements.txt", 'r') as f:
        requirements = f.read()
    
    required_deps = [
        "streamlit",
        "pytest",
        "pytest-cov",
        "coverage",
        "black",
        "isort",
        "bandit",
        "safety",
    ]
    
    all_passed = True
    for dep in required_deps:
        if dep in requirements:
            print(f"✅ {dep}: Found in requirements.txt")
        else:
            print(f"❌ {dep}: Not found in requirements.txt")
            all_passed = False
    
    return all_passed


def validate_import_structure():
    """Validate that imports work correctly."""
    print("\n🔗 Validating Import Structure...")
    
    import_tests = [
        ("from src.models.task import Task", "Task model import"),
        ("from src.services.task_service import TaskService", "TaskService import"),
        ("from src.utils.exceptions import TaskNotFoundException", "Exception import"),
    ]
    
    all_passed = True
    for import_stmt, description in import_tests:
        try:
            exec(import_stmt)
            print(f"✅ {description}: SUCCESS")
        except ImportError as e:
            print(f"❌ {description}: FAILED - {e}")
            all_passed = False
        except Exception as e:
            print(f"❌ {description}: ERROR - {e}")
            all_passed = False
    
    return all_passed


def main():
    """Main validation function."""
    print("🚀 Task Manager Project Validation")
    print("=" * 50)
    
    # Change to the project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    validation_results = []
    
    # Run all validations
    validation_results.append(validate_github_workflow())
    validation_results.append(validate_test_structure())
    validation_results.append(validate_package_structure())
    validation_results.append(validate_dependencies())
    validation_results.append(validate_import_structure())
    
    # Summary
    print("\n📊 Validation Summary")
    print("=" * 50)
    
    passed = sum(validation_results)
    total = len(validation_results)
    
    if passed == total:
        print(f"🎉 All validations passed! ({passed}/{total})")
        print("\n✅ Your project is ready for CI/CD!")
        print("✅ The GitHub Actions workflow will:")
        print("   - Use the latest action versions (no more v3 deprecation warnings)")
        print("   - Run comprehensive tests across multiple Python versions")
        print("   - Generate and upload test coverage reports")
        print("   - Perform security analysis")
        print("   - Build and validate distribution packages")
        return 0
    else:
        print(f"⚠️  Some validations failed ({passed}/{total})")
        print("\n❌ Please fix the issues above before pushing to GitHub.")
        return 1


if __name__ == "__main__":
    sys.exit(main())