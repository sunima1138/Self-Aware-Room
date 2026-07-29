"""Raw payload storage for L1 acquisition and reference-based handoff."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Protocol

from ..contracts.identity import generate_object_id


@dataclass(slots=True)
class RawReference:
    """Reference to stored raw evidence."""

    raw_ref_uri: str
    checksum_sha256: str
    media_type: str
    byte_size: int

    def as_payload(self) -> dict[str, Any]:
        """Return a transport-friendly dictionary representation."""
        return {
            "raw_ref_uri": self.raw_ref_uri,
            "checksum_sha256": self.checksum_sha256,
            "media_type": self.media_type,
            "byte_size": self.byte_size,
        }


class RawStore(Protocol):
    """Storage contract for persisting raw capture artifacts."""

    def store_payload(self, source_id: str, payload: dict[str, Any]) -> RawReference:
        """Persist payload and return a stable raw reference."""


class LocalFileRawStore:
    """Filesystem-backed raw store for local development and testing."""

    def __init__(self, base_dir: str = "runtime/raw_observations") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def store_payload(self, source_id: str, payload: dict[str, Any]) -> RawReference:
        """Serialize payload as JSON and return a reference to the stored artifact."""
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        artifact_id = generate_object_id()
        artifact_name = f"{stamp}_{source_id}_{artifact_id}.json"
        artifact_path = self.base_dir / artifact_name

        encoded = json.dumps(payload, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        artifact_path.write_bytes(encoded)

        return RawReference(
            raw_ref_uri=str(artifact_path),
            checksum_sha256=sha256(encoded).hexdigest(),
            media_type="application/json",
            byte_size=len(encoded),
        )
