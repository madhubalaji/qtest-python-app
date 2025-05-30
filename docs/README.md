# Task Manager Documentation

This directory contains comprehensive documentation for the Task Manager application.

## Documentation Structure

- `index.md`: Main documentation page with an overview and quick start guide
- `installation.md`: Detailed installation instructions
- `usage/`: Usage guides
  - `cli.md`: Command-line interface documentation
  - `web.md`: Web interface documentation
- `api/`: API reference
  - `models.md`: Documentation for data models
  - `services.md`: Documentation for services
  - `utils.md`: Documentation for utilities
- `development.md`: Guide for developers
- `contributing.md`: Guidelines for contributing to the project
- `generate_html.py`: Script to generate HTML documentation from Markdown files

## Viewing the Documentation

You can view the documentation in several ways:

1. **Directly in GitHub**: If you're viewing this on GitHub, you can navigate through the Markdown files directly.

2. **In a Markdown viewer**: You can use any Markdown viewer to read the documentation files.

3. **As HTML**: You can generate HTML documentation for easier viewing:

   a. Make the generator script executable:
      ```bash
      chmod +x docs/generate_html.py
      ```

   b. Run the documentation generator:
      ```bash
      python docs/generate_html.py
      ```

   c. Open the generated HTML documentation:
      ```bash
      # On Linux/macOS
      open docs/html/index.html
      
      # On Windows
      start docs/html/index.html
      ```

## Updating the Documentation

When making changes to the Task Manager application, please update the relevant documentation files to keep them in sync with the code.

## Contributing to the Documentation

If you find any issues or have suggestions for improving the documentation, please see the [Contributing Guidelines](contributing.md) for information on how to contribute.