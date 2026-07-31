"""L2 normalization stage scaffold.

This stage standardizes observation payload shape and marks normalization status.
"""

from __future__ import annotations

from ..contracts.identity import Provenance
from ..contracts.models import DataObject, ObjectType, Observation
from ..contracts.stages import StageComponent, StageResult, StageStatus, TelemetryEmitter


class L2NormalizationStage(StageComponent):
    """Normalize L1 observations into canonical observation objects."""

    def __init__(self, telemetry: TelemetryEmitter | None = None) -> None:
        super().__init__(stage_name="L2_Normalization", telemetry=telemetry)

    def accept_input(self, input_objects: list[DataObject]) -> bool:
        return all(obj.object_type == ObjectType.OBSERVATION for obj in input_objects)

    def process(self, input_objects: list[DataObject]) -> StageResult:
        self._emit_received(len(input_objects))
        if not self.accept_input(input_objects):
            self._emit_error("L2 accepts Observation objects only.")
            return StageResult(
                status=StageStatus.ERROR,
                messages=["L2 accepts Observation objects only."],
            )

        output_objects: list[DataObject] = []
        for obj in input_objects:
            normalized_payload = dict(obj.payload)
            normalized_payload.setdefault("normalized", True)

            normalized = Observation(
                source_id=getattr(obj, "source_id", ""),
                trace_id=obj.trace_id,
                quality_status=obj.quality_status or "normalized",
                error_status=obj.error_status,
                payload=normalized_payload,
                time_context=obj.time_context,
                provenance=Provenance(
                    parent_object_ids=[obj.object_id],
                    source_native_id=obj.provenance.source_native_id,
                    created_by_component=self.stage_name,
                    component_version="0.1.0",
                    configuration_version="default",
                ),
            )
            output_objects.append(normalized)

        self._emit_transformed(len(input_objects), len(output_objects))
        self._emit_sent(len(output_objects))

        return StageResult(
            output_objects=output_objects,
            status=StageStatus.OK,
            messages=[f"L2 produced {len(output_objects)} normalized observation(s)."],
        )
