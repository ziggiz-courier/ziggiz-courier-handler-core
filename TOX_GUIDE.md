# Tox Matrix Testing Guide

This guide explains how to use tox to test the Ziggiz-Courier project across multiple Python versions.

## What is Tox?

Tox is a generic virtualenv management and testing command line tool that allows you to test your Python package against multiple Python versions and environments. It automates the process of creating isolated environments, installing dependencies, and running tests.

## Setup

Tox is already configured in this project. The `tox.ini` file defines test environments for:
- Python 3.8 to 3.13
- Linting with black, flake8, and isort
- Type checking with mypy

## Prerequisites

To use tox, you'll need to have all Python versions you want to test against installed on your system. You can use tools like pyenv to manage multiple Python versions:

```bash
# Install pyenv (macOS)
brew install pyenv

# Install Python versions
pyenv install 3.11
pyenv install 3.12
pyenv install 3.13

# Make them available globally
pyenv global system 3.11 3.12 3.13
```

## Running Tests with Tox

### Install tox

```bash
pip install tox tox-poetry
```

### Run tests for all Python versions

```bash
tox
```

### Run tests for a specific Python version

```bash
tox -e py38   # Test on Python 3.8
tox -e py39   # Test on Python 3.9
tox -e py310  # Test on Python 3.10
tox -e py311  # Test on Python 3.11
tox -e py312  # Test on Python 3.12
tox -e py313  # Test on Python 3.13
```

### Run only linting checks

```bash
tox -e lint
```

### Run only type checking

```bash
tox -e mypy
```

### Format code

```bash
tox -e format
```

### Run tests in parallel

```bash
tox -p  # Run all environments in parallel
tox -p -e py38,py39,py310  # Run specific environments in parallel
```

## Configuration

The tox configuration is defined in `tox.ini`. If you need to change test dependencies or add/remove Python versions, edit that file.

## GitHub Actions Integration

The project is configured to run tox tests via GitHub Actions. The workflow is defined in `.github/workflows/tox-matrix.yml` and automatically runs tests for all supported Python versions on pull requests and pushes to main branches.

## Troubleshooting

### Missing Python interpreters

If tox can't find a Python interpreter, make sure it's installed and available in your PATH.

### Dependency issues

If you encounter dependency issues, try cleaning the tox environments:

```bash
tox -r  # Recreate environments
```

### Debugging tox

For verbose output:

```bash
tox -v
```

For seeing what would be done without actually doing it:

```bash
tox --showconfig
```
