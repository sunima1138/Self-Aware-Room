# Self-Aware Room (SAR)

Primary repository for the CHI Self-Aware Room (SAR) project.

Last updated: 2026-07-29

## Current State

This repository now contains active computational scaffolding, formal computational specifications, and subsystem-oriented implementation folders.

## Quick Start (Computational Baseline)

Use this path for first-time local setup and baseline validation:

1. Setup instructions: [D04.02 Setup Instructions](docs/computational/D04.02_SAR_Computational_Pipeline_Setup_Instructions_V1_2026-07-29.md)
2. Computational doc index: [Computational Document Index](docs/computational/README.md)
3. Runnable demo entry point: [pipeline_demo.py](src/sar_apps/pipeline_demo.py)

## Status

Teams assigned to Self-Aware Room:  
- [Self Aware Room Team](https://github.com/orgs/CHI-CityTech/teams/self-aware-room)  
  All members of the SAR project
- [Video Production Team](https://github.com/orgs/CHI-CityTech/teams/video-production)
- [Audio Production Team](https://github.com/orgs/CHI-CityTech/teams/audio-production)
- [Computation Team]() (Currently a stub)
- [Structure Team]()  (Currently a stub)

## Documentation Hierarchy

The documentation set is organized as a multi-track hierarchy.

- [docs/README.md](docs/README.md): top-level documentation index and conventions.
- [docs/computational](docs/computational): Doc-ID-governed computational architecture and implementation specifications.
- [docs/audio](docs/audio): audio-system design and integration documentation.
- [docs/video](docs/video): video/projection and media-pipeline documentation.
- [docs/structure](docs/structure): physical/structural design and integration documentation.
- [docs/assets](docs/assets): shared document assets.
- [docs/archive](docs/archive): superseded drafts and historical references.

## Summer 2026 Scope (Initial)

- Coordinate SAR-facing technical, semantic, and infrastructure work.
- Track baseline system goals for July and extension work for August.
- Consolidate room-system documentation and integration standards.

## Inventory List for integration of purchases

[Inventory final: this will hold all inventory when finished](https://docs.google.com/spreadsheets/d/1xlmzvB_z3JYaaETMTt0t8i_Rfrj9V4yKD3l8Fw04o0s/edit?usp=sharing)  
[OAA Inventory List to pull from and integrate with the main list](https://docs.google.com/spreadsheets/d/1Y4ND_M3c1ZKv1S4Bs0K1mHY8vtbBrymCsntErgicCTM/edit?usp=sharing)

## Related Repositories

### Primary META-Projects

- [META-Blended-Reality-Performance-System](https://github.com/CHI-CityTech/META-Blended-Reality-Performance-System): BRPS meta-layer context linking performance, room systems, and blended-reality integration.
- [META-CHIIDS](https://github.com/CHI-CityTech/META-CHIIDS): broader CHI integrated digital systems framing and architecture context.

### Associated Projects

- [CHI-StudentResearch](https://github.com/CHI-CityTech/CHI-StudentResearch): Summer 2026 operations, student intake, launch planning, and active cohort coordination.
- [Bio-Aware Blended Space (BABS)](https://github.com/CHI-CityTech/BABS): bio-aware blended-spaces work treated as a SAR subset/component where relevant.
- [Unity-BSP](https://github.com/CHI-CityTech/Unity-BSP): digital twin and virtual-physical mapping work connected to SAR room-state modeling.
- [AVMI-GVSC-SoundSystem](https://github.com/CHI-CityTech/AVMI-GVSC-SoundSystem): related audio-routing and room-system infrastructure work where sound deployment overlaps with SAR implementation.
- [Personalized-LLM](https://github.com/CHI-CityTech/Personalized-LLM): related AI/LLM experimentation that may inform SAR semantic and agent-support workflows.
- Blended Shadow Puppet Theatre (link pending): significant overlap with SAR projection, audio, and media integration.

## Relationship Notes

- Self Aware Room is coordinated with Blended Shadow Puppet through BRPS-aligned physical, virtual, media, and semantic integration workstreams.
- BABS is treated as a defined subset/component within SAR when biological-entity interaction, perception, and related semantic interpretation are in scope.
- AVMI-GVSC-SoundSystem is treated as an associated infrastructure project where SAR audio deployment, routing, and room-system integration overlap.
- CHI-StudentResearch remains the active Summer 2026 cohort and operations repository, while this repository is intended to become the primary SAR project repository.

## Repository Layout

- docs/: architecture, roadmap, and subsystem documentation tracks.
- operations/: active planning and execution materials.
- src/: source code for SAR computational pipeline components and demos.
- workstreams/: stream-specific trackers and handoff notes.
- system/: implementation-facing artifacts by subsystem (video, audio, sensors, control, telemetry, structure).

## Student Project Intake

- Student registration cards are submitted through the GitHub issue form: `.github/ISSUE_TEMPLATE/student_project_registration.yml`.
- Intake cards are intended to feed a single tracking spreadsheet schema documented in `operations/student_project_intake_spreadsheet_schema.md`.
- Contact information fields may be partially blank at first submission and completed during intake review.
- First-day discussions focus on confirming first tasks, dependencies, and realistic weekly availability.

## Immediate Next Steps

1. Confirm canonical SAR workstreams and owners.
2. Add the first systems map and integration conventions.
3. Migrate or reference active Summer 2026 materials from CHI-StudentResearch where appropriate.
