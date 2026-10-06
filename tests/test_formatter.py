# Copyright 2026-present Orbit Contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Security and context behavior for Orbit's optional JSON logging formatter."""

import json
import logging

from orbit import Application, ApplicationConfig
from orbit.runtime.context import (
    bind_application,
    bind_correlation_id,
    bind_request_id,
    bind_span_id,
    bind_trace_id,
    reset_application,
    reset_correlation_id,
    reset_request_id,
    reset_span_id,
    reset_trace_id,
)

from orbit_logging import JSONFormatter


def test_formatter_includes_bound_orbit_context_and_excludes_unapproved_data() -> None:
    application = Application(ApplicationConfig(name="logging-test"))
    error = ValueError("password=do-not-log")
    record = logging.LogRecord(
        "test.logger", logging.ERROR, "", 1.0, "operation failed", (), (ValueError, error, None)
    )
    record.authorization = "do-not-log"
    tokens = (
        bind_application(application),
        bind_request_id(application.config.application.id),
        bind_correlation_id("corr-1"),
        bind_trace_id("a" * 32),
        bind_span_id("b" * 16),
    )
    try:
        encoded = JSONFormatter().format(record)
    finally:
        reset_span_id(tokens[4])
        reset_trace_id(tokens[3])
        reset_correlation_id(tokens[2])
        reset_request_id(tokens[1])
        reset_application(tokens[0])

    payload = json.loads(encoded)
    assert payload["logger"] == "test.logger"
    assert payload["message"] == "operation failed"
    assert payload["exception_type"] == "ValueError"
    assert payload["application"] == "logging-test"
    assert payload["application_id"] == str(application.config.application.id)
    assert payload["request_id"] == str(application.config.application.id)
    assert payload["correlation_id"] == "corr-1"
    assert payload["trace_id"] == "a" * 32
    assert payload["span_id"] == "b" * 16
    assert "do-not-log" not in encoded


def test_formatter_works_without_an_active_orbit_application() -> None:
    record = logging.LogRecord("test", logging.INFO, "", 1.0, "ready", (), None)

    payload = json.loads(JSONFormatter().format(record))

    assert payload["message"] == "ready"
    assert payload["request_id"] is None
    assert "application" not in payload


def test_formatter_does_not_include_exception_message() -> None:
    error = RuntimeError("sensitive-detail")
    record = logging.LogRecord(
        "test", logging.ERROR, "", 1.0, "operation failed", (), (RuntimeError, error, None)
    )

    payload = json.loads(JSONFormatter().format(record))

    assert payload["exception_type"] == "RuntimeError"
    assert "sensitive-detail" not in json.dumps(payload)


def test_formatter_truncates_oversized_log_messages() -> None:
    """One oversized record cannot produce an unbounded JSON message field."""
    record = logging.LogRecord("test", logging.INFO, "", 1.0, "x" * 20_000, (), None)

    payload = json.loads(JSONFormatter().format(record))

    assert len(payload["message"]) == 16_384 + len("... [truncated]")
    assert payload["message"].endswith("... [truncated]")
