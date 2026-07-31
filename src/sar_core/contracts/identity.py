"""Identity and provenance primitives for SAR contract objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def generate_object_id() -> str:
    """Return a stable string object identifier.

    UUIDv7 is preferred in SAR docs, but Python stdlib support may vary by runtime.
    This helper uses UUID4 for now and centralizes the policy for easy upgrade.
    """
    return str(uuid4())


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Provenance:
    """Trace linkage for derived objects across pipeline stages."""

    parent_object_ids: list[str] = field(default_factory=list)
    source_native_id: str | None = None
    created_by_component: str | None = None
    component_version: str | None = None
    configuration_version: str | None = None
