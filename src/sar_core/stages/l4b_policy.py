"""L4B policy and decision stage scaffold."""

from __future__ import annotations

from ..contracts.identity import Provenance
from ..contracts.models import DataObject, Decision, Intent, ObjectType
from ..contracts.stages import StageComponent, StageResult, StageStatus, TelemetryEmitter


class L4BPolicyStage(StageComponent):
    """Produce a primitive decision and intent from semantic state."""

    def __init__(self, telemetry: TelemetryEmitter | None = None) -> None:
        super().__init__(stage_name="L4B_Policy", telemetry=telemetry)

    def accept_input(self, input_objects: list[DataObject]) -> bool:
        return all(obj.object_type == ObjectType.SEMANTIC_STATE for obj in input_objects)

    def process(self, input_objects: list[DataObject]) -> StageResult:
        self._emit_received(len(input_objects))
        if not self.accept_input(input_objects):
            self._emit_error("L4B accepts SemanticState objects only.")
            return StageResult(
                status=StageStatus.ERROR,
                messages=["L4B accepts SemanticState objects only."],
            )
        if not input_objects:
            self._emit_indeterminate("L4B received no semantic state; no decision emitted.", input_count=0)
            return StageResult(
                status=StageStatus.INDETERMINATE,
                messages=["L4B received no semantic state; no decision emitted."],
            )

        output_objects: list[DataObject] = []
        for semantic in input_objects:
            parent_ids = [semantic.object_id]
            decision = Decision(
                policy_result="observe_only",
                quality_status="provisional_policy",
                payload={"semantic_label": semantic.payload.get("semantic_label", semantic.semantic_label)},
                provenance=Provenance(
                    parent_object_ids=parent_ids,
                    created_by_component=self.stage_name,
                    component_version="0.1.0",
                    configuration_version="default",
                ),
            )
            intent = Intent(
                intent_name="noop_observe",
                quality_status="provisional_intent",
                payload={"decision_object_id": decision.object_id},
                provenance=Provenance(
                    parent_object_ids=[semantic.object_id, decision.object_id],
                    created_by_component=self.stage_name,
                    component_version="0.1.0",
                    configuration_version="default",
                ),
            )
            output_objects.extend([decision, intent])

        self._emit_transformed(len(input_objects), len(output_objects))
        self._emit_sent(len(output_objects))

        return StageResult(
            output_objects=output_objects,
            status=StageStatus.OK,
            messages=[f"L4B emitted {len(output_objects)} decision/intent object(s)."],
        )
