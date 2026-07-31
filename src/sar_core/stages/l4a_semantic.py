"""L4A semantic interpretation stage scaffold."""

from __future__ import annotations

from ..contracts.identity import Provenance
from ..contracts.models import DataObject, ObjectType, SemanticState
from ..contracts.stages import StageComponent, StageResult, StageStatus, TelemetryEmitter


class L4ASemanticStage(StageComponent):
    """Produce a coarse semantic state from coherent state inputs."""

    def __init__(self, telemetry: TelemetryEmitter | None = None) -> None:
        super().__init__(stage_name="L4A_Semantic", telemetry=telemetry)

    def accept_input(self, input_objects: list[DataObject]) -> bool:
        allowed = {ObjectType.STATE, ObjectType.EVENT, ObjectType.ENTITY}
        return all(obj.object_type in allowed for obj in input_objects)

    def process(self, input_objects: list[DataObject]) -> StageResult:
        self._emit_received(len(input_objects))
        if not self.accept_input(input_objects):
            self._emit_error("L4A accepts State/Event/Entity objects only.")
            return StageResult(
                status=StageStatus.ERROR,
                messages=["L4A accepts State/Event/Entity objects only."],
            )
        if not input_objects:
            self._emit_indeterminate("L4A received no input objects; no semantic state emitted.", input_count=0)
            return StageResult(
                status=StageStatus.INDETERMINATE,
                messages=["L4A received no input objects; no semantic state emitted."],
            )

        parent_ids = [obj.object_id for obj in input_objects]
        semantic = SemanticState(
            semantic_label="room_activity_unknown",
            quality_status="provisional_semantics",
            payload={"input_count": len(input_objects), "semantic_version": "0.1.0"},
            provenance=Provenance(
                parent_object_ids=parent_ids,
                created_by_component=self.stage_name,
                component_version="0.1.0",
                configuration_version="default",
            ),
        )

        self._emit_transformed(len(input_objects), 1)
        self._emit_sent(1)

        return StageResult(
            output_objects=[semantic],
            status=StageStatus.OK,
            messages=["L4A emitted provisional semantic state."],
        )
