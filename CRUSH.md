# SuperClaude Framework - Development Guide

## Build/Test/Lint Commands
```bash
# Install development dependencies
pip install -e ".[dev]"

# Code formatting (Black, 88 char line length)
black SuperClaude setup

# Linting
flake8 SuperClaude setup

# Type checking
mypy SuperClaude setup

# Run all quality checks
black . && flake8 SuperClaude setup && mypy SuperClaude setup

# Test installation (dry-run)
SuperClaude install --dry-run --verbose

# Build package
python -m build

# Validate PyPI readiness
python scripts/validate_pypi_ready.py
```

## Code Style Guidelines
- **Formatter**: Black (88 char lines), target Python 3.8-3.12
- **Imports**: Standard library → third-party → local (absolute imports preferred)
- **Type hints**: Required for all public functions using `typing` module
- **Naming**: PascalCase for classes, snake_case for functions/variables, UPPER_SNAKE_CASE for constants
- **Private methods**: Leading underscore (`_method_name`)
- **Docstrings**: Google style with Args/Returns/Raises sections
- **Error handling**: Use specific exceptions, log with `get_logger()`, display user messages with `display_*` functions
- **No comments**: Code should be self-documenting unless explicitly needed

## Project Structure
- `SuperClaude/`: Framework instruction files (Markdown-based AI prompts)
- `setup/`: Installation system (components, services, utils, CLI)
- `scripts/`: Build and publishing utilities
- Config files: `pyproject.toml` (main config), `setup.py` (legacy support)