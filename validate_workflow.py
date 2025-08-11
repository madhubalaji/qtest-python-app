#!/usr/bin/env python3
"""
Validate the GitHub Actions workflow file.
"""

import yaml
import sys
import os

def validate_workflow():
    """Validate the GitHub Actions workflow YAML file."""
    workflow_path = ".github/workflows/python-app.yml"
    
    if not os.path.exists(workflow_path):
        print(f"✗ Workflow file not found: {workflow_path}")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        print("✓ Workflow YAML is valid")
        
        # Check required fields
        required_fields = ['name', 'on', 'jobs']
        for field in required_fields:
            if field not in workflow:
                print(f"✗ Missing required field: {field}")
                return False
        
        print("✓ Required fields present")
        
        # Check jobs
        jobs = workflow.get('jobs', {})
        if not jobs:
            print("✗ No jobs defined")
            return False
        
        print(f"✓ Found {len(jobs)} jobs: {list(jobs.keys())}")
        
        # Check for actions/upload-artifact usage
        artifact_actions = []
        for job_name, job_config in jobs.items():
            steps = job_config.get('steps', [])
            for step in steps:
                if 'uses' in step and 'upload-artifact' in step['uses']:
                    artifact_actions.append((job_name, step['uses']))
        
        if artifact_actions:
            print("✓ Found artifact upload actions:")
            for job, action in artifact_actions:
                print(f"  - {job}: {action}")
                if '@v4' in action:
                    print(f"    ✓ Using latest version (v4)")
                elif '@v3' in action:
                    print(f"    ⚠ Using deprecated version (v3)")
                else:
                    print(f"    ? Unknown version")
        
        # Check Python versions in matrix
        test_job = jobs.get('test', {})
        strategy = test_job.get('strategy', {})
        matrix = strategy.get('matrix', {})
        python_versions = matrix.get('python-version', [])
        
        if python_versions:
            print(f"✓ Testing on Python versions: {python_versions}")
        else:
            print("⚠ No Python version matrix found")
        
        return True
        
    except yaml.YAMLError as e:
        print(f"✗ YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"✗ Validation error: {e}")
        return False

def check_action_versions():
    """Check if all GitHub Actions are using recommended versions."""
    workflow_path = ".github/workflows/python-app.yml"
    
    recommended_versions = {
        'actions/checkout': 'v4',
        'actions/setup-python': 'v5',
        'actions/cache': 'v4',
        'actions/upload-artifact': 'v4',
        'codecov/codecov-action': 'v4'
    }
    
    try:
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        print("\nChecking action versions:")
        for action, recommended in recommended_versions.items():
            if action in content:
                if f"{action}@{recommended}" in content:
                    print(f"✓ {action}: using recommended version {recommended}")
                else:
                    print(f"⚠ {action}: not using recommended version {recommended}")
            else:
                print(f"- {action}: not used")
        
        return True
    except Exception as e:
        print(f"✗ Error checking action versions: {e}")
        return False

def main():
    """Main validation function."""
    print("=" * 60)
    print("GitHub Actions Workflow Validator")
    print("=" * 60)
    
    success = True
    
    if not validate_workflow():
        success = False
    
    if not check_action_versions():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✓ Workflow validation passed!")
        return 0
    else:
        print("✗ Workflow validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())