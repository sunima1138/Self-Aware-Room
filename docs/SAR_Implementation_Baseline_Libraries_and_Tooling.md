# SAR Implementation Baseline: Libraries, Tooling, and Engineering Delivery

*Document Class:* Implementation Baseline Specification  
*Project:* Self-Aware-Room (SAR)  
*Status:* Draft for build planning  
*Date:* 2026-07-18

## 1. Purpose

This section defines the implementation baseline needed to turn the generalized SAR computational pipeline into working software while preserving architectural clarity.

### 1.1 Objective

This subsection states the practical objective of this document as an implementation guide for student researchers and technical leads.

Define a concrete set of competencies, base libraries, tooling standards, and deliverables required to build SAR pipeline software as a maintainable program or program set.

### 1.2 Relationship to Existing Specifications

This subsection clarifies where this baseline document fits in the specification stack.

- This document supports the generalized architecture in [SAR_General_Computational_Pipeline_Spec_V1_2026-07-18.md](SAR_General_Computational_Pipeline_Spec_V1_2026-07-18.md).
- This document does not replace the design baseline PDF dated 2026-04-27.
- This document prepares follow-on component specifications and implementation work.

## 2. Researcher Competency Profile

This section defines minimum and preferred competencies for a student researcher implementing the SAR computational framework.

### 2.1 Required Core Competencies

This subsection lists capabilities that must be present at project start.

- Python programming across modules, packages, and virtual environments.
- Object-oriented design fundamentals and interface-based programming.
- Basic design pattern literacy for modular architecture.
- Git workflow competency with branch-based development.
- Ability to read and author technical documentation and diagrams.

### 2.2 Required OOP and Pattern Literacy

This subsection defines pattern-level fluency expected for pipeline implementation.

- Adapter pattern for sensor-specific ingestion wrappers.
- Strategy pattern for interchangeable processing behaviors.
- Factory pattern for component construction by configuration.
- Observer or event-bus style for decoupled inter-layer signaling.
- Command pattern for output dispatch actions.

### 2.3 Preferred Supporting Competencies

This subsection identifies useful capabilities that reduce implementation risk.

- Familiarity with real-time or near-real-time data handling.
- Basic signal processing intuition for audio and sensor noise.
- Prior use of structured logging and runtime diagnostics.
- Experience with unit testing and integration testing in Python.

## 3. Implementation Form: Program Set and Potential Library

This section defines how the software should be organized initially and when an internal library should be extracted.

### 3.1 Initial Form

This subsection defines the recommended starting architecture.

Begin as a modular program set with clear package boundaries, keeping framework logic separate from sensor adapters and execution runners.

### 3.2 Internal Library Trigger Criteria

This subsection defines when to extract and maintain an internal SAR library.

Extract a shared internal library only after:

1. at least two sensor modalities use the same interface contracts,
2. coherence/integration interfaces are stable across test cases,
3. semantics and output layers can consume shared state contracts without local patching.

### 3.3 Suggested Package Topology

This subsection proposes a baseline package structure for implementation planning.

- `sar_core`: contracts, base models, common utilities.
- `sar_acquisition`: adapters and source connectors.
- `sar_normalization`: modality normalization logic.
- `sar_coherence`: alignment, correlation, and conflict resolution.
- `sar_semantics`: rules and interpretation scaffolding.
- `sar_dispatch`: output routing and safety enforcement.
- `sar_apps`: runnable entry points, demos, and controlled test runners.

## 4. Base Libraries and Tooling Baseline

This section provides a practical baseline stack for Python implementation and maintainability.

### 4.1 Runtime and Data Libraries

This subsection lists core runtime libraries for early implementation.

- `pydantic`: typed contracts and schema validation.
- `numpy`: vector and array handling.
- `sounddevice`: live audio ingestion.
- `opencv-python`: camera/video capture pathways where needed.
- `websockets` or `pyzmq`: inter-process and control messaging.
- `python-dotenv`: environment configuration loading.

### 4.2 Reliability and Observability Libraries

This subsection lists libraries for resilience and diagnostics.

- `structlog` (or equivalent) for structured event logs.
- `tenacity` for controlled retries around I/O boundaries.
- standard `logging` integration for compatibility and export.

### 4.3 Testing and Quality Tooling

This subsection defines baseline quality gates, including unit testing.

- `pytest` for test execution and fixtures.
- `pytest-asyncio` where async flows are used.
- `mypy` for static type checking.
- `ruff` for linting and formatting.

### 4.4 Packaging and Environment Baseline

This subsection defines baseline environment and dependency management.

- `pyproject.toml` as single source of package/tool config.
- `uv` or Poetry for dependency and environment management.
- reproducible local setup instructions in repository docs.

## 5. Testing Strategy Baseline

This section defines the minimum testing expectations for SAR implementation artifacts.

### 5.1 Unit Testing Policy

This subsection defines unit testing as a required engineering practice.

Unit testing is required for each computational layer and for shared contracts. New logic should include tests for nominal behavior, edge cases, and failure behavior.

### 5.2 Integration Testing Policy

This subsection defines expected integration checks across layer boundaries.

Integration tests should validate end-to-end handoff across at least one full vertical slice, from acquisition through dispatch, for each active test case.

### 5.3 Contract and Regression Testing

This subsection defines protection against interface drift and behavioral regressions.

- Contract tests must verify packet and state schemas between layers.
- Regression tests must capture previously resolved defects.
- Test fixtures should include representative noisy or incomplete inputs.

### 5.4 Coverage Expectations

This subsection defines practical coverage targets for early-phase implementation.

- Prioritize high-risk modules (coherence, dispatch, schema transforms).
- Use coverage thresholds as guidance, not as sole quality signal.
- Require test evidence for merges touching core interfaces.

## 6. UML and Design Artifact Baseline

This section defines required UML artifacts and their intended review purpose.

### 6.1 Minimum UML Artifact Set

This subsection lists required diagrams for architecture and implementation alignment.

1. Component diagram for L1-L6 layer boundaries.
2. Package diagram for module ownership and dependencies.
3. Class diagram for major interfaces and core abstractions.
4. Sequence diagram for intake-to-coherence flow.
5. Sequence diagram for coherence-to-semantics-to-dispatch flow.

### 6.2 Diagram Governance

This subsection defines how UML artifacts remain useful during implementation.

- Diagrams must be versioned with specification updates.
- Diagram updates are required when interface boundaries change.
- Diagram references should appear in related specification documents.

## 7. Applications and Execution Targets

This section defines practical execution forms for implementation and validation.

### 7.1 Initial Execution Targets

This subsection lists recommended early application forms.

- CLI runner for local deterministic test runs.
- Scripted scenario runner for regression and replay.
- Optional API wrapper only after core contracts stabilize.

### 7.2 Integration with Existing Creative Systems

This subsection identifies likely integration endpoints for SAR outputs.

- TouchDesigner control/event endpoints.
- QLab or equivalent cue/transport endpoints.
- Structured logs and telemetry outputs for review workflows.

## 8. Deliverables for the First Implementation Cycle

This section defines concrete deliverables for the first student implementation cycle.

### 8.1 Engineering Deliverables

This subsection lists implementation artifacts required for cycle completion.

1. Modular Python codebase aligned to layer boundaries.
2. Documented interface contracts for each layer handoff.
3. Unit and integration test suites with execution instructions.
4. Baseline UML artifact set.
5. Short technical report describing assumptions and unresolved risks.

### 8.2 Review Gate

This subsection defines completion criteria for moving to expanded sensor specifications.

Proceed to additional sensor-specific specifications only after:

- contract stability is demonstrated,
- coherence layer behavior is testable and documented,
- basic output dispatch path is validated,
- core test suite is repeatable by another team member.

## 9. Next Authoring Steps

This section defines immediate follow-on documentation actions.

### 9.1 Short-Term Sequence

This subsection lists the recommended next specification actions.

1. Refine the generalized pipeline spec with deeper detail per layer.
2. Align Sensor Intake Phase 1 as Test Case 01 to updated contracts.
3. Author Coherence and Integration detailed specification.
4. Author Semantics and Decisioning detailed specification.
5. Author output-stage detailed specifications by subsystem.
