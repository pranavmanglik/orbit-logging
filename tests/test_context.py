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
"""Orbit logging context extraction remains explicit and detached."""

from uuid import uuid4

from orbit.runtime.context import bind_correlation_id, bind_request_id, bind_span_id, bind_trace_id

from orbit_logging import current_log_context


def test_current_log_context_copies_only_known_identifiers() -> None:
    request_id = uuid4()
    tokens = (
        bind_request_id(request_id),
        bind_correlation_id("corr-1"),
        bind_trace_id("a" * 32),
        bind_span_id("b" * 16),
    )
    try:
        context = current_log_context()
        assert context["request.id"] == str(request_id)
        assert context["correlation.id"] == "corr-1"
        assert context["trace.id"] == "a" * 32
        assert context["span.id"] == "b" * 16
        assert "secret" not in repr(context)
    finally:
        from orbit.runtime.context import (
            reset_correlation_id,
            reset_request_id,
            reset_span_id,
            reset_trace_id,
        )

        reset_span_id(tokens[3])
        reset_trace_id(tokens[2])
        reset_correlation_id(tokens[1])
        reset_request_id(tokens[0])
