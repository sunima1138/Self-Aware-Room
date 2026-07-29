"""O1 observability scaffold for status and trace collection."""

from __future__ import annotations

from ..contracts.observability import LogLevel, LogRecord
from ..contracts.stages import StageStatus
from ..observability_sinks import LogSink


class O1ObservabilityComponent:
    """In-memory telemetry emitter for early integration testing."""

    def __init__(self, sinks: list[LogSink] | None = None) -> None:
        self.records: list[LogRecord] = []
        self.sinks: list[LogSink] = sinks or []

    def emit_status(self, stage_name: str, status: StageStatus, message: str) -> None:
        self._publish(
            LogRecord(
                stage_name=stage_name,
                record_type="status",
                level=LogLevel.INFO,
                message=message,
                payload={"status": status.value},
            )
        )

    def emit_trace(self, stage_name: str, input_count: int, output_count: int) -> None:
        self._publish(
            LogRecord(
                stage_name=stage_name,
                record_type="trace",
                level=LogLevel.DEBUG,
                message="Stage transform trace",
                payload={"input_count": input_count, "output_count": output_count},
            )
        )

    def _publish(self, record: LogRecord) -> None:
        self.records.append(record)
        for sink in self.sinks:
            sink.emit(record)
