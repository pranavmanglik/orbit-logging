# Orbit Logging: operations

`orbit-logging` has no runtime settings, environment variables, or handlers of its own. The
application configures Python logging and attaches `JSONFormatter` to the handlers that should emit
Orbit context.

## Handler setup

Configure levels, filters, propagation, stream/file destinations, rotation, and redaction at the
application boundary. Importing `orbit_logging` does not modify the root logger. When configuring
the same logger at multiple levels, check propagation to avoid duplicate records. Attach separate
formatter instances per handler if sinks need different formatting.

The formatter runs synchronously as part of `Handler.emit`. A slow file system or remote sink can
block the calling thread, including an async request thread. For high-throughput services, use a
queue-based logging setup or nonblocking handler managed by the application. Bound the queue and
define its overflow and shutdown policy.

## Output and downstream systems

Each call returns one compact JSON string. Configure the sink to preserve one complete JSON record
per line and to avoid adding an incompatible prefix. Ensure downstream parsers tolerate optional
application/context fields and the exception-type-only representation. The formatter does not
include a traceback, so use a separate explicitly approved diagnostic path if traceback retention is
required; review that path for sensitive data.

Messages are truncated after 16,384 characters, but this happens after Python constructs the
formatted message. Keep messages concise before they reach the formatter. Logger, level, and
exception class labels are also bounded. Context IDs are populated only when Core has bound them to
the current async context.

## Retention and delivery

This package does not rotate files, encrypt records, retry sink delivery, buffer during outages, or
guarantee durable writes. Configure retention, access controls, encryption, backup, delivery
monitoring, and shutdown flushing in the chosen handler or collector. Avoid sending the same
record to multiple sinks with different data-retention policies unless each sink is approved for
that data.
