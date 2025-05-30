# Installation Guide

This guide provides detailed instructions for installing the Task Manager application.

## Prerequisites

Before installing the Task Manager, ensure you have the following prerequisites:

- Python 3.6 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Installation Methods

### Method 1: Install from Source

1. Clone the repository (or download the source code):
   ```bash
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

### Method 2: Install using pip

If the package is published on PyPI, you can install it directly using pip:

```bash
pip install task-manager
```

## Verifying the Installation

To verify that the Task Manager has been installed correctly, you can run:

```bash
task-manager --version
```

Or, if you installed from source:

```bash
python -m src.cli --version
```

## Configuration

The Task Manager stores tasks in a JSON file located in the `config` directory. By default, this file is named `tasks.json`. You can specify a different file path when initializing the `TaskService` class.

## Troubleshooting

If you encounter any issues during installation, try the following:

1. Ensure you have the correct Python version:
   ```bash
   python --version
   ```

2. Update pip to the latest version:
   ```bash
   pip install --upgrade pip
   ```

3. If you're using a virtual environment, ensure it's activated:
   ```bash
   # For venv
   source venv/bin/activate  # On Unix/macOS
   venv\Scripts\activate     # On Windows
   
   # For conda
   conda activate your-env-name
   ```

4. Check for any error messages in the console output and refer to the error message for specific issues.

If you continue to experience issues, please [open an issue](https://github.com/yourusername/task-manager/issues) on the GitHub repository.