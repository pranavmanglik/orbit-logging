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
"""JSON formatting for standard-library log records with Orbit request context."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime

_MAX_MESSAGE_LENGTH = 16_384
_TRUNCATION_MARKER = "... [truncated]"


class JSONFormatter(logging.Formatter):
    """Format a log event as JSON with Orbit identity and request correlation.

    Only stable, explicitly selected fields are serialized. Exception messages, stack locals and
    arbitrary ``LogRecord`` extras are excluded to reduce accidental disclosure.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Serialize one record without implicitly collecting credentials or payload data."""
        from orbit.runtime.context import (
            current_application,
            current_correlation_id,
            current_request_id,
            current_span_id,
            current_trace_id,
        )

        application = current_application()
        request_id = current_request_id()
        message = record.getMessage()
        if len(message) > _MAX_MESSAGE_LENGTH:
            message = message[:_MAX_MESSAGE_LENGTH] + _TRUNCATION_MARKER
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": message,
            "request_id": str(request_id) if request_id is not None else None,
            "correlation_id": current_correlation_id(),
            "trace_id": current_trace_id(),
            "span_id": current_span_id(),
        }
        if application is not None:
            payload["application_id"] = str(application.config.application.id)
            payload["application"] = application.config.application.name
        if record.exc_info and record.exc_info[0] is not None:
            payload["exception_type"] = record.exc_info[0].__name__
        return json.dumps(payload, ensure_ascii=True, allow_nan=False)


__all__ = ["JSONFormatter"]
