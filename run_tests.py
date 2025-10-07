#!/usr/bin/env python3
"""
Test runner script to verify the implementation.
"""

import sys
import os
import subprocess

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

def run_import_tests():
    """Run basic import and functionality tests."""
    print("=" * 50)
    print("Running Import and Basic Functionality Tests")
    print("=" * 50)
    
    try:
        exec(open('test_imports.py').read())
        return True
    except Exception as e:
        print(f"Import tests failed: {e}")
        return False

def run_pytest():
    """Run the full pytest suite."""
    print("\n" + "=" * 50)
    print("Running Full Test Suite with pytest")
    print("=" * 50)
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', '-v', '--tb=short'
        ], capture_output=True, text=True, cwd='.')
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return code: {result.returncode}")
        return result.returncode == 0
        
    except Exception as e:
        print(f"pytest execution failed: {e}")
        return False

def main():
    """Main test runner."""
    print("Task Manager Delete Functionality Test Suite")
    print("=" * 60)
    
    # Run import tests first
    import_success = run_import_tests()
    
    if not import_success:
        print("\n❌ Import tests failed. Cannot proceed with full test suite.")
        return False
    
    # Run full test suite
    pytest_success = run_pytest()
    
    if pytest_success:
        print("\n✅ All tests passed successfully!")
        print("✅ Delete functionality implementation is ready!")
    else:
        print("\n❌ Some tests failed. Please check the output above.")
    
    return pytest_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)