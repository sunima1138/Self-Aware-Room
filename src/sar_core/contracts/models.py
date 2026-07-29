"""Shared SAR object model aligned with computational architecture documents.

This module defines transport/data artifacts exchanged between computational
stages. Stage/layer processing components should implement stage interfaces
rather than inherit from these object models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable

from .identity import Provenance, generate_object_id
from .timing import TimeContext


class ObjectType(str, Enum):
    """Canonical SAR object categories.

    These values align with the architecture documents and are intended to be
    stable across layer boundaries.
    """

    OBSERVATION = "observation"
    EVENT = "event"
    ENTITY = "entity"
    STATE = "state"
    SEMANTIC_STATE = "semantic_state"
    DECISION = "decision"
    INTENT = "intent"
    EXECUTION_PLAN = "execution_plan"
    DISPATCH = "dispatch"
    EVALUATION_RECORD = "evaluation_record"


@dataclass(slots=True)
class DataObject:
    """Common fields across all SAR contract objects.

    Each specialized object extends this base contract and fixes ``object_type``
    in ``__post_init__``.

    This base class is for pipeline data artifacts, not for stage/layer
    processing components.
    """

    object_type: ObjectType = field(init=False, default=ObjectType.OBSERVATION)
    object_id: str = field(default_factory=generate_object_id)
    trace_id: str | None = None
    quality_status: str | None = None
    error_status: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    provenance: Provenance = field(default_factory=Provenance)
    time_context: TimeContext = field(default_factory=TimeContext)

    def __post_init__(self) -> None:
        """Prevent direct use of this base class as a transport artifact."""
        if self.__class__ is DataObject:
            raise TypeError("DataObject is abstract; instantiate a concrete subtype")


@dataclass(slots=True)
class Observation(DataObject):
    """Source-derived measurement or source-local frame from L1/L2.

    Observations are raw and/or normalized source evidence.
    """

    source_id: str = ""

    def __post_init__(self) -> None:
        DataObject.__post_init__(self)
        self.object_type = ObjectType.OBSERVATION


@dataclass(slots=True)
class Event(DataObject):
    """Correlated occurrence candidate produced by coherence/integration (L3).

    Purpose:
    - represent a bounded "something happened" hypothesis that can be consumed
      by state construction and later semantic interpretation.

    Aggregation model:
    - derived from one or more Observation objects after temporal/spatial alignment,
    - combines multi-source evidence into a single event hypothesis by reference,
    - preserves lineage in provenance for audit and replay.

    Scope linkage:
    - room_entity_id links the event to the canonical room entity context.
    """

    event_type: str | None = None
    room_entity_id: str | None = None
    observation_ids: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        DataObject.__post_init__(self)
        self.object_type = ObjectType.EVENT

        # Keep event aggregation inputs explicit and mirrored in provenance.
        for observation_id in self.observation_ids:
            if observation_id not in self.provenance.parent_object_ids:
                self.provenance.parent_object_ids.append(observation_id)

    def add_observation_id(self, observation_id: str) -> None:
        """Add one observation ID and mirror it into provenance."""
        if observation_id not in self.observation_ids:
            self.observation_ids.append(observation_id)
        if observation_id not in self.provenance.parent_object_ids:
            self.provenance.parent_object_ids.append(observation_id)

    def add_observation_ids(self, observation_ids: Iterable[str]) -> None:
        """Add multiple observation IDs and mirror them into provenance."""
        for observation_id in observation_ids:
            self.add_observation_id(observation_id)


@dataclass(slots=True)
class Entity(DataObject):
    """Tracked entity representation, typically produced by L3.

    The room itself may be represented as a canonical singleton entity.
    """

    entity_type: str | None = None
    room_entity_id: str | None = None
    is_canonical_room: bool = False

    def __post_init__(self) -> None:
        DataObject.__post_init__(self)
        self.object_type = ObjectType.ENTITY


@dataclass(slots=True)
class State(DataObject):
    """Bounded state estimate emitted from coherence/integration layers."""

    state_scope: str | None = None
    room_entity_id: str | None = None

    def __post_init__(self) -> None:
        DataObject.__post_init__(self)
        self.object_type = ObjectType.STATE


@dataclass(slots=True)
class SemanticState(DataObject):
    """Interpreted representation of system meaning from L4A."""

    semantic_label: str | None = None

    def __post_init__(self) -> None:
        DataObject.__post_init__(self)
        self.object_type = ObjectType.SEMANTIC_STATE


@dataclass(slots=True)
class Decision(DataObject):
    """Policy-evaluated response decision from L4B."""

    policy_result: str | None = None

    def __post_init__(self) -> None:
        DataObject.__post_init__(self)
        self.object_type = ObjectType.DECISION


@dataclass(slots=True)
class Intent(DataObject):
    """Abstract response request passed into orchestration."""

    intent_name: str | None = None

    def __post_init__(self) -> None:
        DataObject.__post_init__(self)
        self.object_type = ObjectType.INTENT


@dataclass(slots=True)
class ExecutionPlan(DataObject):
    """Ordered action plan prepared for dispatch execution."""

    steps: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        DataObject.__post_init__(self)
        self.object_type = ObjectType.EXECUTION_PLAN


@dataclass(slots=True)
class Dispatch(DataObject):
    """Channel-specific command routed to an output endpoint."""

    channel: str | None = None

    def __post_init__(self) -> None:
        DataObject.__post_init__(self)
        self.object_type = ObjectType.DISPATCH


@dataclass(slots=True)
class EvaluationRecord(DataObject):
    """Trace, metric, or diagnostic artifact emitted to O1 workflows."""

    metric_name: str | None = None

    def __post_init__(self) -> None:
        DataObject.__post_init__(self)
        self.object_type = ObjectType.EVALUATION_RECORD


def create_canonical_room_entity(
    room_entity_id: str = "room_main",
    *,
    room_name: str = "main_room",
    coordinate_frame: str | None = "room_frame",
    payload: dict[str, Any] | None = None,
) -> Entity:
    """Create the canonical singleton room entity for the running system."""
    room_payload: dict[str, Any] = {"room_name": room_name}
    if coordinate_frame is not None:
        room_payload["coordinate_frame"] = coordinate_frame
    if payload:
        room_payload.update(payload)

    return Entity(
        entity_type="room",
        room_entity_id=room_entity_id,
        is_canonical_room=True,
        payload=room_payload,
    )
