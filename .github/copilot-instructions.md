# Ziggiz-Courier Development Guidelines

## Project Overview

The Ziggiz-Courier project implements data processing pipelines for transforming various log formats, with a focus on syslog messages (RFC3164, RFC5424), JSON, CSV, and XML formats.

## Code Structure

- **Decoders**: Parse raw log formats into structured model objects
- **Models**: Data structures representing parsed log messages
- **Adapters**: Transform between different model formats
- **Encoders**: Convert model objects to output formats (JSON, etc.)

## Development Standards

### General Coding Standards
- Follow PEP 8 for Python code style
- Use type hints for function signatures and class attributes
- Use f-strings for string formatting as a last resort where appropriate such as logging use a dict i.e extra
- Use `isinstance()` for type checking
- Avoid using `eval()` and `exec()`
- Use `with` statements for file handling
- Use `logging` for logging instead of print statements
- Use `pytest` for testing
- Use `mypy` for type checking
- Use `black` for code formatting
- Use `flake8` for linting
- Use `isort` for sorting imports

### Regex Standards
- Use raw strings for regex patterns (e.g., `r"pattern"`)
- Use named groups for better readability (e.g., `(?P<name>pattern)`)
- Avoid overly complex regex patterns; break them into smaller components if necessary
- Use `re.compile()` for frequently used patterns to improve performance
- Document regex patterns with comments explaining their purpose
- Use `re.match()` for matching at the start of a string
- Use `re.search()` for searching anywhere in the string
- Use `re.findall()` for finding all occurrences of a pattern
- Use `re.sub()` for replacing patterns in strings
- Use `re.split()` for splitting strings based on patterns
- Use `re.escape()` to escape special characters in strings
- Use `re.finditer()` for iterating over matches in a string
- Use `re.subn()` to get the number of substitutions made
- Use `re.fullmatch()` for matching the entire string


### Logging Standards
- Use `logging` module for logging
- Use different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Use `logging.getLogger(__name__)` to get a logger for the current module
- Use `logging.basicConfig()` to configure the logging
- Use `logging.Formatter` to format log messages
- Use `logging.StreamHandler` for console output
- Format console logging using json

### Exception Handling
- Use custom exceptions for specific error cases
- Use `try`/`except` blocks for error handling
- Use `finally` blocks for cleanup actions
- Use `raise` to propagate exceptions
- Use `assert` statements for debugging and testing
- Use `contextlib` for context managers
- Use `functools.wraps` for decorators to preserve metadata
- Use `traceback` for detailed error reporting
- Use `warnings` for non-critical issues
- Use `logging.exception()` for logging exceptions
- Use `logging.error()` for logging errors
- Use `logging.warning()` for logging warnings
- Use `logging.info()` for logging informational messages
- Use `logging.debug()` for logging debug messages
- Use the "Extra" keyword argument for logging to add additional context avoid using f-strings in logging messages

### Testing Requirements

- **Unit Tests**: Test a single component in isolation
  - Mark with `@pytest.mark.unit`
  - Include both positive and negative test cases
  - Use parameterized tests for similar test cases
- **Integration Tests**: Test multiple components together
  - Mark with `@pytest.mark.integration`
  - Focus on end-to-end flows
- **Feature-Specific Tests**:
  - Use `@pytest.mark.rfc3164` for BSD syslog format tests
  - Use `@pytest.mark.rfc5424` for modern syslog format tests

### Documentation Standards

- Include docstrings for all public methods and classes
- Document Args, Returns, and Raises sections
- Document timestamp formats and parsing rules
- Maintain clear examples in the examples/ directory

### Code Organization

- Import order: standard library, third-party, local/package imports
- Consistent naming conventions:
  - Classes: PascalCase
  - Functions/methods: snake_case
  - Constants: UPPER_SNAKE_CASE
- Maintain proper inheritance hierarchies:
  - BaseModel → SyslogRFCBaseModel → format-specific models

### Common Issues to Avoid

- **Circular Imports**: Be careful with imports in **init**.py files
- **Interface Changes**: Update all relevant tests when changing interfaces
- **Test Isolation**: Unit tests should not depend on other components
- **Import Errors**: Check for missing or incorrect imports before committing

## How to Add New Components

### Adding a New Decoder

1. Implement a new class inheriting from `Decoder[YourModel]`
2. Provide a `decode()` method returning your model type
3. Add unit tests with `@pytest.mark.unit`
4. Document supported formats and parsing rules

### Adding a New Model

1. Implement a new class inheriting from appropriate base model
2. Define clear data structure with type hints
3. Add validation logic if needed
4. Add unit tests with `@pytest.mark.unit`

### Adding a New Adapter

1. Implement a new class inheriting from `Adapter[SourceModel, TargetModel]`
2. Provide a `transform()` method converting between models
3. Add unit tests with `@pytest.mark.unit`

### Adding a New Encoder

1. Implement a new class inheriting from `Encoder[YourModel]`
2. Provide an `encode()` method producing the output format
3. Add unit tests with `@pytest.mark.unit`
