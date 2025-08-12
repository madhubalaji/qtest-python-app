#!/usr/bin/env python3
"""
Simple script to run tests and verify they work.
"""

import sys
import os
import subprocess

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

def run_tests():
    """Run the test suite."""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 'tests/', '-v'
        ], capture_output=True, text=True, cwd='/workspace')
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)