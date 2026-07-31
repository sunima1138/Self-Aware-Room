"""Edge ingress contracts for distributed sensors (e.g., ESP32)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .identity import Provenance
from .models import Observation
from .timing import TimeContext


@dataclass(slots=True)
class EdgeObservationFrame:
    """Network transport frame emitted by an edge capture node.

    This is intentionally lightweight and transport-oriented. Gateways map this
    frame to internal Observation objects at ingest time.
    """

    source_node_id: str
    source_id: str
    modality: str
    encoding: str
    sample_rate_hz: int
    channel_count: int
    frame_index: int
    payload: dict[str, Any]
    source_capture_time: datetime | None = None
    source_frame_id: str | None = None
    source_latency_ms: float | None = None


def observation_from_edge_frame(frame: EdgeObservationFrame) -> Observation:
    """Convert an edge transport frame into a source Observation."""
    source_frame_id = frame.source_frame_id or f"{frame.source_node_id}:{frame.frame_index}"
    return Observation(
        source_id=frame.source_id,
        quality_status="raw_capture",
        provenance=Provenance(source_native_id=source_frame_id),
        time_context=TimeContext(source_capture_time=frame.source_capture_time),
        payload={
            "source_node_id": frame.source_node_id,
            "modality": frame.modality,
            "encoding": frame.encoding,
            "sample_rate_hz": frame.sample_rate_hz,
            "channel_count": frame.channel_count,
            "frame_index": frame.frame_index,
            "source_frame_id": source_frame_id,
            "source_latency_ms": frame.source_latency_ms,
            **frame.payload,
        },
    )
