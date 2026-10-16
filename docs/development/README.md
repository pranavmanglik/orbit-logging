# Orbit Logging: development

This package adapts Orbit task-local context to Python's standard logging record format. Keep the
public field schema deliberate, bounded, and independent of private Core internals.

## Local setup and checks

From the repository root:

```bash
python -m pip install -e '.[dev]' build
pytest
ruff check src tests
ruff format --check src tests
mypy
python -m build
```

The tests use in-memory `LogRecord` values and Core context bindings; they require no external log
collector. They cover field inclusion/exclusion, context propagation, message bounds, and output
label handling, but do not exercise a configured production handler or sink.

## Formatter change guidance

- Select fields explicitly. Do not serialize `record.__dict__`, arbitrary `extra` fields, or
  traceback text by default.
- Bound and sanitize fields that can be controlled by a caller or dynamic runtime value.
- Keep message truncation and output valid JSON, including for Unicode and exception records.
- Add tests that prove secrets are absent from the serialized line, not only from the returned
  Python object.
- Preserve Core public-context boundaries; avoid importing private runtime variables.
- Document any schema field addition because collectors and dashboards consume the output shape.

Follow the contribution guide, governance, code of conduct, and security policy. Keep fixtures
synthetic and report local validation separately from hosted CI and live collector behavior.
