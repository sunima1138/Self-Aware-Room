"""Base stage interfaces for SAR computational pipeline components."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol

from .models import DataObject


class StageStatus(str, Enum):
    OK = "ok"
    DEGRADED = "degraded"
    INDETERMINATE = "indeterminate"
    ERROR = "error"


@dataclass(slots=True)
class StageResult:
    """Standard response from a stage transform."""

    output_objects: list[DataObject] = field(default_factory=list)
    status: StageStatus = StageStatus.OK
    messages: list[str] = field(default_factory=list)


class TelemetryEmitter(Protocol):
    """Cross-cutting observer contract (O1-compatible)."""

    def emit_status(self, stage_name: str, status: StageStatus, message: str) -> None:
        ...

    def emit_trace(self, stage_name: str, input_count: int, output_count: int) -> None:
        ...


class StageComponent(ABC):
    """Interface-first base class for layer components."""

    stage_name: str
    telemetry: TelemetryEmitter | None

    def __init__(self, stage_name: str, telemetry: TelemetryEmitter | None = None) -> None:
        self.stage_name = stage_name
        self.telemetry = telemetry

    def _emit_received(self, input_count: int) -> None:
        if self.telemetry is None:
            return
        self.telemetry.emit_status(self.stage_name, StageStatus.OK, f"Received {input_count} object(s).")

    def _emit_transformed(self, input_count: int, output_count: int) -> None:
        if self.telemetry is None:
            return
        self.telemetry.emit_status(
            self.stage_name,
            StageStatus.OK,
            f"Transformed {input_count} object(s) into {output_count} object(s).",
        )
        self.telemetry.emit_trace(self.stage_name, input_count=input_count, output_count=output_count)

    def _emit_sent(self, output_count: int) -> None:
        if self.telemetry is None:
            return
        self.telemetry.emit_status(self.stage_name, StageStatus.OK, f"Sent {output_count} object(s).")

    def _emit_error(self, message: str) -> None:
        if self.telemetry is None:
            return
        self.telemetry.emit_status(self.stage_name, StageStatus.ERROR, message)

    def _emit_indeterminate(self, message: str, input_count: int) -> None:
        if self.telemetry is None:
            return
        self.telemetry.emit_status(self.stage_name, StageStatus.INDETERMINATE, message)
        self.telemetry.emit_trace(self.stage_name, input_count=input_count, output_count=0)

    @abstractmethod
    def accept_input(self, input_objects: list[DataObject]) -> bool:
        """Validate whether this stage can process the incoming objects."""

    @abstractmethod
    def process(self, input_objects: list[DataObject]) -> StageResult:
        """Transform input objects according to stage responsibility."""
