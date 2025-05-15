# Courier Data Processing

A Python library for decoding, transforming, and encoding data in various formats.

## Overview

The Courier Data Processing library provides a flexible framework for processing data across different formats and protocols. It follows a modular architecture with:

- **Decoders**: Convert raw input data (strings, bytes, etc.) into strongly-typed data models
- **Models**: Pydantic-based data classes with validation
- **Adapters**: Transform data between different model types
- **Encoders**: Convert models to different output formats

## Features

- **Multiple Format Support**: Process data from Syslog, JSON, CSV, and XML formats
- **Transformation Pipeline**: Decode → Transform → Encode workflow
- **Unified Event Model**: Common event model for standardizing different data formats
- **OpenTelemetry Integration**: Export events as OpenTelemetry spans
- **Flexible & Extensible**: Easy to add new decoders, adapters, and encoders
- **Type Safety**: Leverages Python type hints and Pydantic for type validation
- **Continuous Integration/Deployment**: Automated testing, linting, and releases

## Installation

```bash
# Using Poetry (recommended)
poetry add core-data-processing

# Using pip
pip install core-data-processing
```

## Quick Start

### Process a Syslog Message to JSON

```python
from core_data_processing import SyslogRFC5424Decoder, SyslogToCommonEventAdapter, JSONEncoder

# Create the components
decoder = SyslogRFC5424Decoder()
adapter = SyslogToCommonEventAdapter()
encoder = JSONEncoder()

# Process a syslog message
syslog_message = '<34>1 2023-05-09T02:33:52.123Z myhostname app 1234 ID47 [exampleSDID@32473 iut="3"] An application event log entry'

# Pipeline processing: decode -> adapt -> encode
decoded = decoder.decode(syslog_message)
common_event = adapter.transform(decoded)
json_output = encoder.encode(common_event)

print(json_output)
```

### Process JSON Data

```python
from core_data_processing import JSONLogDecoder, JSONEncoder

# Create the components
decoder = JSONLogDecoder()
encoder = JSONEncoder()

# Process a JSON log
json_log = '{"id":"12345","timestamp":"2023-05-09T13:45:30Z","level":"error","message":"Connection timed out","host":"webserver-01"}'

# Pipeline processing: decode -> encode
event = decoder.decode(json_log)
json_output = encoder.encode(event)

print(json_output)
```

### Process CSV Data

```python
from core_data_processing import CSVLogDecoder, JSONEncoder

# Create the components
decoder = CSVLogDecoder()
encoder = JSONEncoder()

# Process CSV log data with header row
csv_data = """timestamp,message,severity,system,component
2023-05-09T13:45:30Z,Test message,warning,test-system,test-component"""

# Pipeline processing: decode -> encode
events = decoder.decode(csv_data)
for event in events:
    json_output = encoder.encode(event)
    print(json_output)
```

### Process XML Data

```python
from core_data_processing import XMLLogDecoder, JSONEncoder

# Create the components
decoder = XMLLogDecoder()
encoder = JSONEncoder()

# Process XML log data
xml_data = """
<events>
    <event id="event-123">
        <timestamp>2023-05-09T13:45:30Z</timestamp>
        <message>Login successful</message>
        <severity>INFO</severity>
        <system>auth-server</system>
        <component>login-service</component>
    </event>
</events>"""

# Pipeline processing: decode -> encode
events = decoder.decode(xml_data)
for event in events:
    json_output = encoder.encode(event)
    print(json_output)
```

### Process a Syslog Message to OpenTelemetry

```python
from opentelemetry.sdk.trace import TracerProvider
from core_data_processing import SyslogRFC5424Decoder, SyslogToCommonEventAdapter, OtelSpanEncoder

# Initialize OpenTelemetry
tracer_provider = TracerProvider()
# Configure exporters as needed...

# Create the components
decoder = SyslogRFC5424Decoder()
adapter = SyslogToCommonEventAdapter()
encoder = OtelSpanEncoder(tracer_provider)

# Process a syslog message
syslog_message = '<34>1 2023-05-09T02:33:52.123Z myhostname app 1234 ID47 [exampleSDID@32473 iut="3"] An application event log entry'

# Pipeline processing: decode -> adapt -> encode
decoded = decoder.decode(syslog_message)
common_event = adapter.transform(decoded)
span = encoder.encode(common_event)
# Span will be automatically exported based on tracer provider configuration
```

## Complete Pipeline Example

Here's an example of a complete data processing pipeline that:

1. Decodes data from a source format
2. Transforms it to a common model
3. Encodes it to a destination format

```python
from core_data_processing import (
    SyslogRFC5424Decoder, SyslogToCommonEventAdapter,
    JSONEncoder, OtelSpanEncoder
)
from opentelemetry.sdk.trace import TracerProvider

# Initialize components
decoder = SyslogRFC5424Decoder()
adapter = SyslogToCommonEventAdapter()
json_encoder = JSONEncoder()
tracer_provider = TracerProvider()
otel_encoder = OtelSpanEncoder(tracer_provider)

# Sample input data
syslog_message = '<34>1 2023-05-09T02:33:52.123Z myhostname app 1234 ID47 [exampleSDID@32473 iut="3"] An application event log entry'

# Process through pipeline
syslog_parsed = decoder.decode(syslog_message)
common_event = adapter.transform(syslog_parsed)

# Output to multiple destinations
json_output = json_encoder.encode(common_event)
otel_span = otel_encoder.encode(common_event)

print(f"JSON Output: {json_output}")
print(f"OpenTelemetry Span: {otel_span}")
```

## Architecture

The library is designed around the following components:

### Decoders

Decoders transform raw data (strings, bytes, etc.) into structured data models:

```python
from core_data_processing import Decoder, SyslogRFC5424Message

class CustomDecoder(Decoder[SyslogRFC5424Message]):
    def decode(self, raw_data: str) -> SyslogRFC5424Message:
        # Custom decoding logic
        ...
        return syslog_message
```

### Models

Models are Pydantic classes that represent data structures with validation:

```python
from core_data_processing import EventEnvelopeBaseModel
from typing import Optional

class CustomModel(EventEnvelopeBaseModel):
    field1: str
    field2: int
    optional_field: Optional[str] = None
```

### Adapters

Adapters transform between different model types:

```python
from core_data_processing import Adapter, SyslogRFC5424Message, CommonEvent

class CustomAdapter(Adapter[SyslogRFC5424Message, CommonEvent]):
    def transform(self, source: SyslogRFC5424Message) -> CommonEvent:
        # Custom transformation logic
        ...
        return common_event
```

### Encoders

Encoders convert models to different output formats:

```python
from core_data_processing import Encoder, CommonEvent

class CustomEncoder(Encoder[CommonEvent, dict]):
    def encode(self, model: CommonEvent) -> dict:
        # Custom encoding logic
        ...
        return data_dict
```

## Available Decoders

- **SyslogRFC5424Decoder**: Parses RFC5424 syslog messages
- **JSONLogDecoder**: Parses JSON-formatted logs
- **CSVLogDecoder**: Parses CSV log files with headers
- **XMLLogDecoder**: Parses XML log data

## Available Encoders

- **JSONEncoder**: Converts events to JSON format
- **OtelSpanEncoder**: Converts events to OpenTelemetry spans

## Development

### Commit Conventions

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification. All commit messages must follow this format to ensure proper versioning and changelog generation.

See [COMMIT_CONVENTION.md](COMMIT_CONVENTION.md) for detailed guidelines.

### Continuous Integration/Deployment

The project uses GitHub Actions for CI/CD:

- **Automated Testing**: All tests are run automatically on push to main branches
- **Code Quality**: Black, Flake8, isort, and mypy are used to ensure code quality
- **Automatic Releases**: New versions are automatically published when:
  - Code changes are pushed to main
  - Dependencies are updated
  - Tests pass successfully

The version number follows semantic versioning and is automatically determined based on commit messages:
- `fix:` commits trigger a PATCH release
- `feat:` commits trigger a MINOR release
- `BREAKING CHANGE:` in commit body triggers a MAJOR release

### Development Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure tests pass locally: `poetry run pytest`
5. Commit using conventional commit format
6. Submit a Pull Request

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request following the guidelines above.

## License

[MIT License](LICENSE)
