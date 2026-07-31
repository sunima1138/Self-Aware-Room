"""Observability contracts shared across SAR components."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from .identity import utc_now


class LogLevel(str, Enum):
    """Minimal severity levels for structured log records."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(slots=True)
class LogRecord:
    """Canonical structured log record for O1 and runtime diagnostics."""

    stage_name: str
    record_type: str
    message: str
    level: LogLevel = LogLevel.INFO
    timestamp_utc: datetime = field(default_factory=utc_now)
    trace_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
