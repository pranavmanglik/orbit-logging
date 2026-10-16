# Orbit Logging

`orbit-logging` is an optional structured logging integration for Orbit Core. It provides a
standard-library `logging.Formatter` that adds Orbit's task-local application, request, correlation,
trace and span context to each JSON record.

```bash
pip install orbit-core orbit-logging
```

Attach the formatter to a handler configured by your application or hosting environment:

```python
import logging

from orbit_logging import JSONFormatter

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.getLogger("my_service").addHandler(handler)
```

Importing this package does not configure the root logger or create handlers. Records include the
explicit message and exception type, but omit exception messages, stack locals, and arbitrary
`LogRecord` extras. Messages above 16,384 characters are truncated with a marker. Keep secrets out
of the message passed to the logging API as well.

The formatter depends on Core's public runtime-context accessors; it does not add an exporter,
logging backend, or transport. Install a separate integration for those capabilities if needed.

## Status

This package is alpha; its API is not stable and it is not yet a published release. It supports
Python 3.11 through 3.14.

## Documentation

The package-specific guides cover [architecture](docs/architecture/overview.md), [operations and security](docs/operations/README.md), and [development](docs/development/README.md), with [security guidance](docs/security/overview.md). The [documentation index](docs/README.md) links to the full package overview and project policies.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
mypy
```

Licensed under Apache-2.0.

