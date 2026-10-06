# Orbit Logging: architecture and boundaries

## Responsibility

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

## Declared dependencies

The following dependency declarations come from the checked-in manifests. Optional groups and development dependencies are called out separately.

### `pyproject.toml`
- `orbit-core>=0.1.0a1,<0.2`
- Optional `dev` group: `pytest>=8,<10`, `ruff>=0.8,<1`, `mypy>=1.13,<2`.

Declared dependencies do not mean that optional providers or services are bundled with this package.

## Implementation layout

Representative implementation files in this checkout:

- `src/orbit_logging/__init__.py`
- `src/orbit_logging/formatter.py`

## Public contract and scope

## Status

This package is pre-alpha; its API is not stable and it is not yet a published release. It supports
Python 3.11 through 3.14.

## Boundary rules

Keep provider SDKs, credentials, transports, and provider-specific error translation in provider adapters. Keep reusable capability contracts in the matching capability package and lifecycle orchestration in Core. Apply the relevant layer for this repository and preserve the dependency direction shown above.
