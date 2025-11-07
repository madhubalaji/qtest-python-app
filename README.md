# Task Manager

A simple task management application with both CLI and web interfaces.

## Features

- Add, view, update the tasks
- Mark tasks as complete
- Search for tasks by keyword
- Filter tasks by status and priority
- Command-line interface for quick task management
- Web interface built with Streamlit for a user-friendly experience

## Project Structure

```
task_manager_project/
├── config/                 # Configuration files and task storage
├── docs/                   # Documentation
├── src/                    # Source code
│   ├── models/             # Data models
│   │   └── task.py         # Task model
│   ├── services/           # Business logic
│   │   └── task_service.py # Task management service
│   ├── utils/              # Utility modules
│   │   └── exceptions.py   # Custom exceptions
│   ├── app.py              # Streamlit web application
│   └── cli.py              # Command-line interface
└── requirements.txt        # Project dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd task_manager_project
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command-line Interface

Run the CLI application:

```
python -m src.cli
```

Available commands:

- Add a task: `python -m src.cli add "Task title" -d "Task description" -p high`
- List tasks: `python -m src.cli list`
- List all tasks including completed: `python -m src.cli list -a`
- Complete a task: `python -m src.cli complete <task-id>`
- Delete a task: `python -m src.cli delete <task-id>`
- Search for tasks: `python -m src.cli search <keyword>`
- View task details: `python -m src.cli view <task-id>`

### Web Interface

Run the Streamlit web application:

```
streamlit run src/app.py
```

The web interface provides the following pages:
- View Tasks: Display and manage all tasks
- Add Task: Create new tasks
- Search Tasks: Find tasks by keyword



## Development

### Setting up the Development Environment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd task_manager_project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

Run specific test files:
```bash
pytest tests/test_task_model.py
pytest tests/test_task_service.py
```

### Code Quality

Format code with Black:
```bash
black .
```

Check code formatting:
```bash
black --check --diff .
```

Run linting with flake8:
```bash
flake8 .
```

### Using Makefile

The project includes a Makefile for common development tasks:

```bash
make help          # Show available commands
make install       # Install dependencies
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run linting
make format        # Format code
make format-check  # Check formatting
make clean         # Clean generated files
make build         # Build package
make all-checks    # Run all quality checks
make ci            # Run full CI pipeline locally
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment. The workflow:

1. **Multi-platform Testing**: Tests run on Ubuntu, Windows, and macOS
2. **Multi-version Support**: Tests against Python 3.8, 3.9, 3.10, 3.11, and 3.12
3. **Code Quality Checks**: 
   - Linting with flake8
   - Code formatting with Black
   - Test coverage reporting
4. **Build Verification**: Package building and validation
5. **Coverage Reporting**: Integration with Codecov for coverage tracking

### Workflow Triggers

- **Push to main/develop**: Full test suite and build
- **Pull Requests**: Full test suite for validation
- **Manual Trigger**: Available through GitHub Actions UI

### Quality Gates

- **Test Coverage**: Minimum 85% coverage required
- **Code Style**: Black formatting and flake8 linting must pass
- **Multi-platform**: Tests must pass on all supported platforms
- **Multi-version**: Tests must pass on all supported Python versions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite (`make all-checks`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please ensure all tests pass and maintain code coverage above 85%.

## License

[MIT License](LICENSE)
