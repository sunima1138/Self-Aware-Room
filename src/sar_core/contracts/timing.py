"""Time and synchronization metadata fields used across SAR objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class TimeContext:
    """Required and optional time fields aligned with SAR D01.01 policy."""

    source_capture_time: datetime | None = None
    receipt_time: datetime | None = None
    processing_time: datetime | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    dispatch_time: datetime | None = None
    completion_time: datetime | None = None
    clock_offset_estimate: float | None = None
    clock_quality: str | None = None
    sync_source: str | None = None
