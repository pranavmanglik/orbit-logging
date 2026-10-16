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
"""Read bounded Orbit request context for structured logging adapters."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

_MAX_CONTEXT_VALUE = 512


def current_log_context() -> Mapping[str, str]:
    """Return detached, bounded Orbit context fields for a log record.

    Only explicit application and request identifiers are returned. Authorization data, request
    bodies, arbitrary context variables, and secret values are never inspected. Callers should
    still treat IDs and application names as potentially sensitive operational metadata.
    """
    from orbit.runtime.context import (
        current_application,
        current_correlation_id,
        current_request_id,
        current_span_id,
        current_trace_id,
    )

    raw: dict[str, object | None] = {
        "application.id": None,
        "application.name": None,
        "request.id": current_request_id(),
        "correlation.id": current_correlation_id(),
        "trace.id": current_trace_id(),
        "span.id": current_span_id(),
    }
    application = current_application()
    if application is not None:
        raw["application.id"] = application.config.application.id
        raw["application.name"] = application.config.application.name
    result: dict[str, str] = {}
    for key, value in raw.items():
        if value is None:
            continue
        text = str(value)
        if len(text) > _MAX_CONTEXT_VALUE:
            text = text[:_MAX_CONTEXT_VALUE]
        if any(ord(character) < 32 or ord(character) == 127 for character in text):
            continue
        result[key] = text
    return MappingProxyType(result)


__all__ = ["current_log_context"]
