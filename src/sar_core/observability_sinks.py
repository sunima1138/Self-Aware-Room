"""Output sinks for O1 log records."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
import json
from pathlib import Path
from typing import Protocol

from .contracts.observability import LogLevel, LogRecord


class LogSink(Protocol):
    """Sink contract for routing structured log records."""

    def emit(self, record: LogRecord) -> None:
        ...


def _level_value(level: LogLevel) -> int:
    ordering = {
        LogLevel.DEBUG: 10,
        LogLevel.INFO: 20,
        LogLevel.WARNING: 30,
        LogLevel.ERROR: 40,
    }
    return ordering[level]


def _should_emit(record_level: LogLevel, minimum_level: LogLevel) -> bool:
    return _level_value(record_level) >= _level_value(minimum_level)


def log_record_to_dict(record: LogRecord) -> dict[str, object]:
    """Convert a LogRecord to a JSON-serializable dictionary."""
    encoded = asdict(record)
    timestamp = encoded.get("timestamp_utc")
    if isinstance(timestamp, datetime):
        encoded["timestamp_utc"] = timestamp.isoformat()
    level = encoded.get("level")
    if isinstance(level, LogLevel):
        encoded["level"] = level.value
    return encoded


class ConsoleLogSink:
    """Emit log records to terminal output in a compact line format."""

    def __init__(self, minimum_level: LogLevel = LogLevel.INFO) -> None:
        self.minimum_level = minimum_level

    def emit(self, record: LogRecord) -> None:
        if not _should_emit(record.level, self.minimum_level):
            return
        ts = record.timestamp_utc.isoformat()
        print(
            f"[{ts}] [{record.level.value.upper()}] "
            f"[{record.stage_name}] {record.record_type}: {record.message} {record.payload}"
        )


class JsonlFileLogSink:
    """Append structured log records to a JSONL file."""

    def __init__(self, file_path: str = "runtime/logs/o1_events.jsonl", minimum_level: LogLevel = LogLevel.DEBUG) -> None:
        self.file_path = Path(file_path)
        self.minimum_level = minimum_level
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, record: LogRecord) -> None:
        if not _should_emit(record.level, self.minimum_level):
            return
        line = json.dumps(log_record_to_dict(record), separators=(",", ":"), ensure_ascii=True)
        with self.file_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{line}\n")
