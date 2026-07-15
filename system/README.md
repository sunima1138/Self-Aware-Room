# System

Implementation-facing SAR artifacts organized by subsystem.

## Subfolders

- `video/`: media pipeline files, scene mappings, render/export outputs, calibration references.
- `audio/`: routing configs, session files, device presets, and processing profiles.
- `sensors/`: sensor configs, capture schemas, sample datasets, and interface notes.
- `control/`: control logic assets, automation mappings, and integration scripts/specs.
- `telemetry/`: logs, metrics schemas, and room-state trace artifacts.

## Convention

Store source-of-truth implementation artifacts here.
Operational planning belongs in `operations/`, and stream ownership/task tracking belongs in `workstreams/`.
