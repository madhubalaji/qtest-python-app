#!/usr/bin/env python3
"""
Run verification tests for the delete functionality implementation.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd='/workspace')
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🚀 Starting verification tests for delete functionality implementation...")
    
    # Change to workspace directory
    os.chdir('/workspace')
    
    tests = [
        ("python test_implementation.py", "Basic functionality verification"),
        ("python -m pytest tests/test_task_model.py -v", "Task model tests"),
        ("python -m pytest tests/test_task_service.py -v", "Task service tests"),
        ("python -c \"from src.app import main; print('App imports work correctly')\"", "App import verification"),
    ]
    
    results = []
    for command, description in tests:
        success = run_command(command, description)
        results.append((description, success))
    
    print(f"\n{'='*60}")
    print("VERIFICATION SUMMARY")
    print('='*60)
    
    all_passed = True
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description}: {status}")
        if not success:
            all_passed = False
    
    if all_passed:
        print(f"\n🎉 ALL VERIFICATION TESTS PASSED!")
        print("The delete functionality implementation is working correctly.")
    else:
        print(f"\n⚠️  SOME TESTS FAILED")
        print("Please review the errors above and fix any issues.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())