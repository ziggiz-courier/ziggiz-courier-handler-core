# Ziggiz-Courier Development Guidelines

## Project Overview
The Ziggiz-Courier project implements data processing pipelines for transforming various log formats, with a focus on syslog messages (RFC3164, RFC5424), JSON, CSV, and XML formats.

## Code Structure
- **Decoders**: Parse raw log formats into structured model objects
- **Models**: Data structures representing parsed log messages
- **Adapters**: Transform between different model formats
- **Encoders**: Convert model objects to output formats (JSON, etc.)

## Development Standards

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
- **Circular Imports**: Be careful with imports in __init__.py files
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
