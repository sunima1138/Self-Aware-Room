"""L5A orchestration stage scaffold."""

from __future__ import annotations

from ..contracts.identity import Provenance
from ..contracts.models import DataObject, ExecutionPlan, ObjectType
from ..contracts.stages import StageComponent, StageResult, StageStatus, TelemetryEmitter


class L5AOrchestrationStage(StageComponent):
    """Build a primitive execution plan from intents."""

    def __init__(self, telemetry: TelemetryEmitter | None = None) -> None:
        super().__init__(stage_name="L5A_Orchestration", telemetry=telemetry)

    def accept_input(self, input_objects: list[DataObject]) -> bool:
        return all(obj.object_type == ObjectType.INTENT for obj in input_objects)

    def process(self, input_objects: list[DataObject]) -> StageResult:
        self._emit_received(len(input_objects))
        if not self.accept_input(input_objects):
            self._emit_error("L5A accepts Intent objects only.")
            return StageResult(
                status=StageStatus.ERROR,
                messages=["L5A accepts Intent objects only."],
            )
        if not input_objects:
            self._emit_indeterminate("L5A received no intents; no execution plan emitted.", input_count=0)
            return StageResult(
                status=StageStatus.INDETERMINATE,
                messages=["L5A received no intents; no execution plan emitted."],
            )

        output_objects: list[DataObject] = []
        for intent in input_objects:
            plan = ExecutionPlan(
                quality_status="provisional_plan",
                steps=[
                    {
                        "step_id": "step_01",
                        "action": "observe",
                        "channel": "internal",
                        "intent_name": getattr(intent, "intent_name", None),
                    }
                ],
                payload={"intent_object_id": intent.object_id},
                provenance=Provenance(
                    parent_object_ids=[intent.object_id],
                    created_by_component=self.stage_name,
                    component_version="0.1.0",
                    configuration_version="default",
                ),
            )
            output_objects.append(plan)

        self._emit_transformed(len(input_objects), len(output_objects))
        self._emit_sent(len(output_objects))

        return StageResult(
            output_objects=output_objects,
            status=StageStatus.OK,
            messages=[f"L5A emitted {len(output_objects)} execution plan(s)."],
        )
