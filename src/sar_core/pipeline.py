"""Pipeline assembly and execution helpers for SAR stage scaffolds."""

from __future__ import annotations

from dataclasses import dataclass

from .contracts.observability import LogLevel
from .contracts.models import DataObject, ObjectType
from .contracts.stages import StageResult, StageStatus
from .observability_sinks import ConsoleLogSink, JsonlFileLogSink
from .stages import (
    L1AcquisitionStage,
    L2NormalizationStage,
    L3CoherenceStage,
    L4ASemanticStage,
    L4BPolicyStage,
    L5AOrchestrationStage,
    L5BDispatchStage,
    O1ObservabilityComponent,
)
from .storage import LocalFileRawStore, RawStore


@dataclass(slots=True)
class PipelineRunResult:
    """Structured output for one end-to-end pipeline run."""

    l1: StageResult
    l2: StageResult
    l3: StageResult
    l4a: StageResult
    l4b: StageResult
    l5a: StageResult
    l5b: StageResult


class SarPipeline:
    """Primitive constructor-backed SAR pipeline for integration testing."""

    def __init__(
        self,
        *,
        l1: L1AcquisitionStage,
        l2: L2NormalizationStage,
        l3: L3CoherenceStage,
        l4a: L4ASemanticStage,
        l4b: L4BPolicyStage,
        l5a: L5AOrchestrationStage,
        l5b: L5BDispatchStage,
        o1: O1ObservabilityComponent | None = None,
    ) -> None:
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4a = l4a
        self.l4b = l4b
        self.l5a = l5a
        self.l5b = l5b
        self.o1 = o1

    @classmethod
    def default(
        cls,
        *,
        room_entity_id: str = "room_main",
        ingest_node_id: str = "ingest_local",
        raw_store: RawStore | None = None,
        default_source_latency_ms: float = 0.0,
    ) -> SarPipeline:
        """Build the default primitive L1-L5 pipeline with optional O1."""
        if raw_store is None:
            raw_store = LocalFileRawStore()

        o1 = O1ObservabilityComponent(
            sinks=[
                ConsoleLogSink(minimum_level=LogLevel.INFO),
                JsonlFileLogSink(file_path="runtime/logs/o1_events.jsonl", minimum_level=LogLevel.DEBUG),
            ]
        )

        return cls(
            l1=L1AcquisitionStage(
                raw_store=raw_store,
                ingest_node_id=ingest_node_id,
                default_source_latency_ms=default_source_latency_ms,
                telemetry=o1,
            ),
            l2=L2NormalizationStage(telemetry=o1),
            l3=L3CoherenceStage(room_entity_id=room_entity_id, telemetry=o1),
            l4a=L4ASemanticStage(telemetry=o1),
            l4b=L4BPolicyStage(telemetry=o1),
            l5a=L5AOrchestrationStage(telemetry=o1),
            l5b=L5BDispatchStage(telemetry=o1),
            o1=o1,
        )

    def run(self, seed_observations: list[DataObject]) -> PipelineRunResult:
        """Execute one primitive end-to-end pass through L1-L5."""
        r1 = self.l1.process(seed_observations)
        self._emit_transfer("L1", "L2", len(r1.output_objects))

        r2 = self.l2.process(r1.output_objects)
        self._emit_transfer("L2", "L3", len(r2.output_objects))

        r3 = self.l3.process(r2.output_objects)
        l4a_input = self._select_by_type(r3.output_objects, {ObjectType.STATE, ObjectType.EVENT, ObjectType.ENTITY})
        self._emit_transfer("L3", "L4A", len(l4a_input))

        r4a = self.l4a.process(l4a_input)
        l4b_input = self._select_by_type(r4a.output_objects, {ObjectType.SEMANTIC_STATE})
        self._emit_transfer("L4A", "L4B", len(l4b_input))

        r4b = self.l4b.process(l4b_input)
        l5a_input = self._select_by_type(r4b.output_objects, {ObjectType.INTENT})
        self._emit_transfer("L4B", "L5A", len(l5a_input))

        r5a = self.l5a.process(l5a_input)
        l5b_input = self._select_by_type(r5a.output_objects, {ObjectType.EXECUTION_PLAN})
        self._emit_transfer("L5A", "L5B", len(l5b_input))

        r5b = self.l5b.process(l5b_input)
        self._emit_transfer("L5B", "OUT", len(r5b.output_objects))

        return PipelineRunResult(l1=r1, l2=r2, l3=r3, l4a=r4a, l4b=r4b, l5a=r5a, l5b=r5b)

    @staticmethod
    def _select_by_type(objects: list[DataObject], allowed: set[ObjectType]) -> list[DataObject]:
        return [obj for obj in objects if obj.object_type in allowed]

    def _emit_transfer(self, from_stage: str, to_stage: str, count: int) -> None:
        if self.o1 is None:
            return
        self.o1.emit_status("PIPELINE", StageStatus.OK, f"Transferred {count} object(s) {from_stage} -> {to_stage}.")
        self.o1.emit_trace("PIPELINE", input_count=count, output_count=count)
