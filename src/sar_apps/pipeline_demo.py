"""Minimal runnable vertical slice for SAR L1->L5 plus O1 scaffolding."""

from __future__ import annotations

from sar_core.contracts import (
    EdgeObservationFrame,
    create_canonical_room_entity,
    observation_from_edge_frame,
)
from sar_core.pipeline import SarPipeline
from sar_core.storage import LocalFileRawStore


def main() -> None:
    room = create_canonical_room_entity()
    raw_store = LocalFileRawStore()
    pipeline = SarPipeline.default(
        room_entity_id=room.room_entity_id or "room_main",
        ingest_node_id="gateway_pi_01",
        raw_store=raw_store,
        default_source_latency_ms=0.0,
    )

    edge_frame = EdgeObservationFrame(
        source_node_id="esp32_north_01",
        source_id="mic_01",
        modality="audio",
        encoding="pcm16",
        sample_rate_hz=48000,
        channel_count=1,
        frame_index=0,
        payload={"raw_audio_chunk": [0.01, -0.03, 0.02, -0.01, 0.0]},
    )
    seed_observation = observation_from_edge_frame(edge_frame)
    run = pipeline.run([seed_observation])

    print("Room entity:", room.object_id, room.room_entity_id)
    print("L1 status:", run.l1.status, run.l1.messages)
    if run.l1.output_objects:
        print("L1 source node:", run.l1.output_objects[0].payload.get("source_node_id"))
        print("L1 ingest node:", run.l1.output_objects[0].payload.get("ingest_node_id"))
        print("L1 raw ref:", run.l1.output_objects[0].payload.get("raw_ref_uri"))
    print("L2 status:", run.l2.status, run.l2.messages)
    print("L3 status:", run.l3.status, run.l3.messages)
    print("L4A status:", run.l4a.status, run.l4a.messages)
    print("L4B status:", run.l4b.status, run.l4b.messages)
    print("L5A status:", run.l5a.status, run.l5a.messages)
    print("L5B status:", run.l5b.status, run.l5b.messages)

    print("L3 objects:")
    for out in run.l3.output_objects:
        print("-", out.object_type.value, out.object_id, out.payload)

    print("L5B objects:")
    for out in run.l5b.output_objects:
        print("-", out.object_type.value, out.object_id, out.payload)

    if pipeline.o1 is not None:
        print("O1 records:", len(pipeline.o1.records))
        print("O1 log file:", "runtime/logs/o1_events.jsonl")


if __name__ == "__main__":
    main()
