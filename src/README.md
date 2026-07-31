# src

This directory contains SAR computational implementation artifacts.

Intended contents include:

- Python packages and modules for the computational pipeline
- Shared contracts, models, and utilities used by runtime code
- Adapters or services for acquisition, normalization, coherence, semantics, orchestration, and dispatch
- Supporting implementation files that belong to the executable system rather than the documentation set

Document-support assets should remain under `docs/`, especially `docs/assets/`.

Current baseline implementation includes active scaffold modules under `sar_core` and a runnable vertical-slice example at `sar_apps/pipeline_demo.py`.
