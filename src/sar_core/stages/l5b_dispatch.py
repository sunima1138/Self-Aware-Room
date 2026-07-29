"""L5B dispatch stage scaffold."""

from __future__ import annotations

from ..contracts.identity import Provenance
from ..contracts.models import DataObject, Dispatch, ObjectType
from ..contracts.stages import StageComponent, StageResult, StageStatus, TelemetryEmitter


class L5BDispatchStage(StageComponent):
    """Emit primitive dispatch objects from execution plans."""

    def __init__(self, telemetry: TelemetryEmitter | None = None) -> None:
        super().__init__(stage_name="L5B_Dispatch", telemetry=telemetry)

    def accept_input(self, input_objects: list[DataObject]) -> bool:
        return all(obj.object_type == ObjectType.EXECUTION_PLAN for obj in input_objects)

    def process(self, input_objects: list[DataObject]) -> StageResult:
        self._emit_received(len(input_objects))
        if not self.accept_input(input_objects):
            self._emit_error("L5B accepts ExecutionPlan objects only.")
            return StageResult(
                status=StageStatus.ERROR,
                messages=["L5B accepts ExecutionPlan objects only."],
            )
        if not input_objects:
            self._emit_indeterminate("L5B received no execution plans; no dispatch emitted.", input_count=0)
            return StageResult(
                status=StageStatus.INDETERMINATE,
                messages=["L5B received no execution plans; no dispatch emitted."],
            )

        output_objects: list[DataObject] = []
        for plan in input_objects:
            dispatch = Dispatch(
                channel="internal",
                quality_status="provisional_dispatch",
                payload={
                    "execution_plan_object_id": plan.object_id,
                    "step_count": len(getattr(plan, "steps", [])),
                },
                provenance=Provenance(
                    parent_object_ids=[plan.object_id],
                    created_by_component=self.stage_name,
                    component_version="0.1.0",
                    configuration_version="default",
                ),
            )
            output_objects.append(dispatch)

        self._emit_transformed(len(input_objects), len(output_objects))
        self._emit_sent(len(output_objects))

        return StageResult(
            output_objects=output_objects,
            status=StageStatus.OK,
            messages=[f"L5B emitted {len(output_objects)} dispatch object(s)."],
        )
