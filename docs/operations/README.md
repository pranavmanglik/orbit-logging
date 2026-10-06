# Orbit Logging: operations and security

This guide organizes runtime behavior documented by the package. It does not certify production readiness. Verify provider/client versions, permissions, transport security, limits, and failure behavior in the target environment before release.

## Configuration surface

Environment names found in the package README:

The package README does not name `ORBIT_*` variables. Use its typed constructors and application configuration, and confirm exact runtime inputs in the implementation before deployment.

Use the package README's constructor and deployment examples. Store credentials in a secret manager and avoid logging credentials, raw provider errors, request data, or opaque cursors.

## Lifecycle, failure behavior, and limits

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

This package is pre-alpha; its API is not stable and it is not yet a published release. It supports
Python 3.11 through 3.14.

## Production validation

Validate startup/shutdown cleanup, timeout and cancellation behavior, concurrency and payload bounds where applicable, secret rotation and least-privilege access, data durability, backup/restore, and failover against the selected provider. Do not infer distributed or durable guarantees from an in-process API or fake-client tests.
