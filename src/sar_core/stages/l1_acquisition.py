"""L1 acquisition stage scaffold.

This stage validates and forwards source observations with minimal shaping.
"""

from __future__ import annotations

from datetime import timedelta

from ..contracts.identity import Provenance
from ..contracts.models import DataObject, ObjectType, Observation
from ..contracts.stages import StageComponent, StageResult, StageStatus, TelemetryEmitter
from ..contracts.timing import TimeContext
from ..contracts.identity import utc_now
from ..storage.raw_store import LocalFileRawStore, RawStore


class L1AcquisitionStage(StageComponent):
    """Initial acquisition stage for source-derived observations."""

    def __init__(
        self,
        raw_store: RawStore | None = None,
        ingest_node_id: str = "ingest_local",
        default_source_latency_ms: float = 0.0,
        telemetry: TelemetryEmitter | None = None,
    ) -> None:
        super().__init__(stage_name="L1_Acquisition", telemetry=telemetry)
        self.raw_store = raw_store
        self.ingest_node_id = ingest_node_id
        self.default_source_latency_ms = default_source_latency_ms

    def accept_input(self, input_objects: list[DataObject]) -> bool:
        return all(obj.object_type == ObjectType.OBSERVATION for obj in input_objects)

    def process(self, input_objects: list[DataObject]) -> StageResult:
        self._emit_received(len(input_objects))
        if not self.accept_input(input_objects):
            self._emit_error("L1 accepts Observation objects only.")
            return StageResult(
                status=StageStatus.ERROR,
                messages=["L1 accepts Observation objects only."],
            )

        output_objects: list[DataObject] = []
        for obj in input_objects:
            now = utc_now()
            payload = dict(obj.payload)
            payload.setdefault("source_node_id", payload.get("source_node_id", "unknown_source_node"))
            payload["ingest_node_id"] = self.ingest_node_id

            source_latency_ms_raw = payload.get("source_latency_ms", self.default_source_latency_ms)
            try:
                source_latency_ms = float(source_latency_ms_raw)
            except (TypeError, ValueError):
                source_latency_ms = self.default_source_latency_ms
            payload["source_latency_ms"] = source_latency_ms

            source_capture_time = obj.time_context.source_capture_time
            if source_capture_time is None:
                source_capture_time = now - timedelta(milliseconds=source_latency_ms)

            receipt_time = obj.time_context.receipt_time or now
            processing_time = now

            # For raw capture chunks, persist once and pass by reference.
            if self.raw_store is not None and "raw_audio_chunk" in payload:
                raw_ref = self.raw_store.store_payload(
                    source_id=getattr(obj, "source_id", "unknown_source"),
                    payload=payload,
                )
                payload = {
                    "source_node_id": payload.get("source_node_id"),
                    "ingest_node_id": self.ingest_node_id,
                    "modality": payload.get("modality", "audio"),
                    "encoding": payload.get("encoding"),
                    "sample_rate_hz": payload.get("sample_rate_hz"),
                    "channel_count": payload.get("channel_count"),
                    "frame_index": payload.get("frame_index"),
                    **raw_ref.as_payload(),
                }

            # Emit a derived observation to maintain explicit lineage.
            derived = Observation(
                source_id=getattr(obj, "source_id", ""),
                trace_id=obj.trace_id,
                quality_status=obj.quality_status or "captured",
                error_status=obj.error_status,
                payload=payload,
                time_context=TimeContext(
                    source_capture_time=source_capture_time,
                    receipt_time=receipt_time,
                    processing_time=processing_time,
                    valid_from=obj.time_context.valid_from,
                    valid_until=obj.time_context.valid_until,
                    dispatch_time=obj.time_context.dispatch_time,
                    completion_time=obj.time_context.completion_time,
                    clock_offset_estimate=obj.time_context.clock_offset_estimate,
                    clock_quality=obj.time_context.clock_quality,
                    sync_source=obj.time_context.sync_source,
                ),
                provenance=Provenance(
                    parent_object_ids=[obj.object_id],
                    source_native_id=obj.provenance.source_native_id
                    or str(payload.get("source_frame_id"))
                    or None,
                    created_by_component=self.stage_name,
                    component_version="0.1.0",
                    configuration_version="default",
                ),
            )
            output_objects.append(derived)

        self._emit_transformed(len(input_objects), len(output_objects))
        self._emit_sent(len(output_objects))

        return StageResult(
            output_objects=output_objects,
            status=StageStatus.OK,
            messages=[f"L1 produced {len(output_objects)} observation(s)."],
        )
