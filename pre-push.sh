#!/bin/bash
# Pre-push hook to run tests before pushing changes

echo "Running tests before pushing..."
pytest

if [ $? -ne 0 ]; then
    echo "Tests failed! Aborting push."
    exit 1
fi

echo "All tests passed. Proceeding with push."
exit 0