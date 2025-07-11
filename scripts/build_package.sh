#!/bin/bash
#
# Script to build the Python package

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python -m build

echo "Package built successfully! Distribution files are in the 'dist' directory."