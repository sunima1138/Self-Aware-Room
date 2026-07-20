# Audio

Audio subsystem implementation artifacts for the Self Aware Room (SAR).

## Purpose

This folder is the source of truth for room-audio implementation assets, routing logic, calibration files, and validation artifacts.

Aligned SAR context:

- Physical room systems layer: audio and routing baseline.
- Virtual/compute systems layer: control mappings and automation hooks.
- Operations cadence: weekly updates during Summer 2026.

## Scope

Store implementation artifacts here, not planning notes.

- Implementation here: configs, exports, presets, and test results.
- Planning in [operations/](../../operations/).
- Owner/task/risk tracking in [workstreams/](../../workstreams/), especially audio-and-routing.

## Suggested Structure

Use subfolders as needed:

- `routing/`: channel maps, bus plans, IO matrices.
- `sessions/`: DAW and playback session exports.
- `presets/`: DSP, mixer, interface, and controller presets.
- `calibration/`: EQ captures, impulse responses, room tuning snapshots.
- `validation/`: test logs, signal-check results, known-good baseline captures.

## Naming Convention

Use predictable names so files can be audited quickly.

- Format: `YYYY-MM-DD_system_topic_version.ext`
- Example: `2026-07-15_roomA_output-routing_v1.csv`
- Avoid ambiguous names like `final` or `new`.

## Integration Interfaces

Document and maintain these handoff points:

- To Control: command contract for mute/solo/scene/state changes.
- To Video: sync references for cues where AV timing matters.
- To Sensors: any audio-reactive or audio-triggered sensor pathways.
- To Telemetry: minimal event/log schema for signal-path and state traces.

## Summer 2026 Deliverables

### M1 Startup Alignment

- Initial system boundary for audio inputs/outputs.
- First version of room routing matrix.
- Owner and dependency list captured in workstreams.

### M2 July Baseline

- Stable baseline playback and routing path validated.
- Calibration snapshot committed.
- Repeatable signal-check procedure documented.

### M3 August Extension

- Extended control paths (adaptive/semantic triggers where in scope).
- Experiment logs and comparison captures archived.

## Definition of Done (per update)

- File names follow convention.
- Changes include date/version metadata.
- Validation artifact is included when routing or calibration changes.
- Relevant dependency or handoff note is updated in workstreams.

## Related SAR Docs

- [SAR architecture overview](../../docs/architecture_overview.md)
- [Summer 2026 roadmap](../../docs/roadmap_summer_2026.md)
- [Workstream conventions](../../workstreams/README.md)
