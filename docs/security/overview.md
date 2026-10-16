# Orbit Logging: security

Logs often have broad access and long retention. `JSONFormatter` reduces accidental disclosure by
excluding arbitrary record extras and exception text, but it cannot determine whether the explicit
message or allowed context is sensitive.

## Message and context data

Do not log passwords, access tokens, cookies, authorization headers, encryption keys, full request
bodies, or unnecessary personal data. Truncation limits size; it does not redact secrets. Prefer
stable error codes and safe identifiers over embedding exception messages in the log message.

Request, correlation, trace, and span values come from Orbit Core's validated context. Application
names are configuration data. Logger and level fields are bounded and have control characters
replaced; JSON escaping prevents them from becoming extra physical log lines. The exception field
contains only a bounded sanitized class label, not the message or traceback. Arbitrary
`LogRecord` extras are intentionally omitted.

The logging sink remains a separate trust boundary. Apply least-privilege access, transport
encryption, at-rest protection, retention/deletion periods, and access auditing in the handler or
collector configuration. Review queue spill files, crash dumps, and diagnostic sinks as log storage
too.

## Error handling and availability

Do not let logging failure expose a second copy of sensitive data through fallback stderr output.
Configure sinks to fail safely and avoid recursive logging from handler error paths. Keep any
asynchronous or queue-based handler bounded so logging cannot exhaust memory during an outage.

Follow the repository [security policy](../../SECURITY.md) for private vulnerability reporting.
This document describes the formatter boundary and is not an audit of the application's log
configuration or storage provider.
