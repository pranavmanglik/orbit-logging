# Orbit Logging: architecture and behavior

## Package boundary

`orbit-logging` is an optional integration for Python's standard-library `logging` package. It
provides `JSONFormatter`, which serializes a selected set of record fields and reads Orbit's
task-local application and request context through Core's public runtime accessors. It does not
configure the root logger, install handlers, write to a sink, export telemetry, or provide a
logging backend.

```text
application logging call ── logging.LogRecord ── handler ── JSONFormatter
                                                       │
                                                       └── Orbit Core task-local context
```

The application or hosting environment owns handlers, filters, levels, propagation, rotation,
queueing, and sink delivery. Install this package only when the application wants the formatter;
Core remains usable without it.

## Record schema

Each output line is one JSON object with an ISO-8601 UTC timestamp, level, logger name, message,
request/correlation/trace/span identifiers, and optional application ID/name. If `exc_info` is
present, the formatter emits an exception class label only. It omits exception messages,
tracebacks, stack locals, and arbitrary `LogRecord` extras.

Message text is truncated after 16,384 characters and marked. Logger name, level, and exception
class labels are bounded and control characters are replaced before encoding. JSON encoding uses
ASCII escapes and disallows non-standard NaN values. Request, correlation, trace, and span IDs are
provided by Core's validated task-local context. Application names and IDs come from Core's
application configuration.

The explicit message is still application-controlled. The formatter cannot infer whether a message
contains a password, access token, personal information, or other secret. Structured logging here
does not mean automatically safe logging; callers must minimize and redact message content.

## Formatter integration

Attach a fresh `JSONFormatter` to a configured handler:

```python
import logging

from orbit_logging import JSONFormatter


handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
service_logger = logging.getLogger("my_service")
service_logger.addHandler(handler)
```

Avoid attaching duplicate handlers when the same record propagates to a parent logger. Do not
format the same record twice for separate sinks if each sink needs a different data-retention or
redaction policy.

## Runtime and performance

Formatting runs synchronously in the handler's thread. A slow network handler attached directly to
an async request path can block that path; use an application-configured queue or nonblocking sink
when required. This package does not create a queue or worker thread. Message formatting via
`LogRecord.getMessage()` happens before truncation, so callers should avoid constructing huge log
messages.

## Source layout and compatibility

- `src/orbit_logging/formatter.py`: selected-field JSON serialization and field bounds.
- `src/orbit_logging/__init__.py`: the `JSONFormatter` public import.

The distribution declares Python `>=3.11,<3.15` and `orbit-core>=0.1.0a1,<0.2`. It is alpha;
see `pyproject.toml` for the authoritative dependency range.
