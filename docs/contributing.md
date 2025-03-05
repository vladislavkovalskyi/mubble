# Contributing to Mubble

Thank you for your interest in contributing to Mubble! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How to Contribute

There are many ways to contribute to Mubble:

1. **Reporting Bugs**: Report bugs by creating an issue on GitHub
2. **Suggesting Features**: Suggest new features or improvements
3. **Writing Code**: Submit pull requests with bug fixes or new features
4. **Improving Documentation**: Help improve the documentation
5. **Reviewing Pull Requests**: Review and comment on open pull requests
6. **Answering Questions**: Help answer questions in discussions and issues

## Reporting Bugs

If you find a bug in Mubble, please report it by creating an issue on GitHub. When reporting a bug, please include:

1. A clear and descriptive title
2. A detailed description of the bug
3. Steps to reproduce the bug
4. Expected behavior
5. Actual behavior
6. Screenshots or code snippets (if applicable)
7. Environment information (Python version, OS, etc.)

## Suggesting Features

If you have an idea for a new feature or an improvement to an existing feature, please create an issue on GitHub. When suggesting a feature, please include:

1. A clear and descriptive title
2. A detailed description of the feature
3. Why the feature would be useful
4. How the feature might be implemented
5. Examples of how the feature would be used

## Development Setup

To set up your development environment for Mubble:

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/mubble.git
   cd mubble
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run tests to ensure your changes don't break existing functionality:
   ```bash
   pytest
   ```
4. Format your code:
   ```bash
   black .
   isort .
   ```
5. Commit your changes with a descriptive commit message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```
6. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Create a pull request on GitHub

## Pull Request Guidelines

When submitting a pull request:

1. Make sure your code passes all tests
2. Update the documentation if necessary
3. Add tests for new features or bug fixes
4. Follow the code style guidelines
5. Keep your pull request focused on a single topic
6. Write a clear and descriptive pull request description
7. Reference any related issues

## Code Style Guidelines

Mubble follows these code style guidelines:

1. Use [Black](https://black.readthedocs.io/) for code formatting
2. Use [isort](https://pycqa.github.io/isort/) for import sorting
3. Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
4. Use type hints for function parameters and return values
5. Write docstrings for all public functions, classes, and methods
6. Keep lines under 88 characters

## Testing

Mubble uses [pytest](https://docs.pytest.org/) for testing. To run the tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=mubble
```

When adding new features or fixing bugs, please add tests to ensure the functionality works correctly.

## Documentation

Mubble's documentation is written in Markdown and located in the `docs` directory. When making changes to the code, please update the documentation accordingly.

To build the documentation locally:

```bash
cd docs
mkdocs build
```

To serve the documentation locally:

```bash
cd docs
mkdocs serve
```

## Release Process

Mubble follows [Semantic Versioning](https://semver.org/). The release process is as follows:

1. Update the version number in `mubble/__init__.py`
2. Update the changelog in `CHANGELOG.md`
3. Create a new release on GitHub
4. Publish the package to PyPI

## Getting Help

If you need help with contributing to Mubble, you can:

1. Join the [Discord server](https://discord.gg/your-discord-server)
2. Ask a question in the GitHub discussions
3. Contact the maintainers directly

## Project Structure

The Mubble project is structured as follows:

```
mubble/
├── mubble/              # Main package
│   ├── __init__.py      # Package initialization
│   ├── api/             # API client
│   ├── bot/             # Bot implementation
│   ├── dispatch/        # Dispatcher
│   ├── handlers/        # Handlers
│   ├── rules/           # Rules
│   ├── types/           # Types
│   └── utils/           # Utilities
├── tests/               # Tests
├── docs/                # Documentation
├── examples/            # Example bots
├── pyproject.toml       # Project configuration
├── README.md            # Project README
└── CHANGELOG.md         # Changelog
```

## License

By contributing to Mubble, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

## Thank You

Thank you for contributing to Mubble! Your help is greatly appreciated. 