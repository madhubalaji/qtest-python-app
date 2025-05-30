# Task Manager Documentation

Welcome to the Task Manager documentation. This documentation provides comprehensive information about the Task Manager application, including installation instructions, usage guides, API references, and development guidelines.

## Overview

Task Manager is a simple task management application with both command-line and web interfaces. It allows you to manage your tasks efficiently by providing features such as adding, viewing, updating, and completing tasks, as well as searching for tasks by keyword and filtering tasks by status and priority.

## Features

- Add, view, and update tasks
- Mark tasks as complete
- Search for tasks by keyword
- Filter tasks by status and priority
- Command-line interface for quick task management
- Web interface built with Streamlit for a user-friendly experience

## Documentation Contents

- [Installation Guide](installation.md): Instructions for installing the Task Manager application
- Usage Guides:
  - [Command-line Interface](usage/cli.md): How to use the command-line interface
  - [Web Interface](usage/web.md): How to use the web interface
- API Reference:
  - [Models](api/models.md): Documentation for data models
  - [Services](api/services.md): Documentation for services
  - [Utilities](api/utils.md): Documentation for utilities
- [Development Guide](development.md): Guide for developers
- [Contributing Guidelines](contributing.md): Guidelines for contributing to the project

## Quick Start

1. Install the Task Manager:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the command-line interface:
   ```bash
   python -m src.cli
   ```

3. Run the web interface:
   ```bash
   streamlit run src/app.py
   ```

## Generating HTML Documentation

This documentation is available in Markdown format, but you can also generate HTML documentation for easier viewing:

1. Install the required dependencies:
   ```bash
   pip install markdown
   ```

2. Run the documentation generator:
   ```bash
   python docs/generate_html.py
   ```

3. Open the generated HTML documentation:
   ```bash
   # On Linux/macOS
   open docs/html/index.html
   
   # On Windows
   start docs/html/index.html
   ```

For more detailed information, please refer to the specific documentation sections.