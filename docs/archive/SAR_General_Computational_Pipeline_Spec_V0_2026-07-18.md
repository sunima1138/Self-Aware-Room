# SAR General Computational Pipeline Specification

*Document Class:* Generalized System Specification  
*Project:* Self-Aware-Room (SAR)  
*Status:* Draft for component-spec baseline  
*Date:* 2026-07-18

## 1. Specification Order

The authoring sequence below keeps SAR computational specifications layered, so each later document extends a stable baseline instead of redefining architecture. The order moves from foundational intent to implementable detail with minimal churn.

### 1.1 Ordered Specification Set

The list below is the official top-down specification path. Following this order lets component teams work in parallel without breaking contract assumptions.

1. Design baseline (unchanged): `Oaa Self-aware Room – Design Specification 2026-04-27.pdf`
2. General computational pipeline spec (this document)
3. Component-level specs (sensor intake, coherence/integration details, semantics/decisioning details, output-stage details)

## 2. Purpose

The purpose below explains why the generalized pipeline document exists and how it should be used in practice. It establishes a common architectural contract for all specialized SAR computational work.

### 2.1 General Objective

The core objective and intended use are to keep the pipeline reusable across modalities while still concrete enough to guide implementation.

Define a generalized but implementable computational pipeline for SAR that all component-specific specifications can inherit from.

### 2.2 Architectural Positioning

The key architectural stance is that coherence and integration are pre-semantics computational work, so semantics can operate on unified state instead of fragmented sensor signals.

This document intentionally introduces a framework-level **Coherence and Integration Layer** that sits before semantics and decisioning.

## 3. Scope

The scope below sets the detail boundary so readers can distinguish what is specified here versus what is deferred to component-level documents. The goal is architectural clarity without premature over-specification.

### 3.1 Included Scope

Included items identify architecture elements that must stay stable across implementations. Together they define the minimum common structure for SAR computational development.

- end-to-end computational layer model,
- packet and interface contracts between layers,
- pre-semantics coherence/integration framework,
- semantics/decisioning role at generalized level,
- output-stage handoff boundaries.

### 3.2 Excluded Scope

Excluded items are intentionally deferred to later specialized specifications. That deferral allows local iteration without destabilizing the generalized model.

- sensor-specific implementation details,
- model-specific prompt or inference tuning,
- production deployment and operations runbooks.

## 4. Layer Model (Generalized)

The layer model below defines the canonical computational flow from raw acquisition to evaluated outputs. It is implementation-facing, so each layer has a clear job, boundary, and handoff.

### 4.1 Pipeline Topology

The topology below is the ordered layer sequence every SAR computational implementation should follow. It reflects a progressive transformation from source evidence to actionable system behavior.

```text
L1 Acquisition
 -> L2 Normalization
 -> L3 Coherence and Integration
 -> L4 Semantics and Decisioning
 -> L5 Orchestration and Output Dispatch
 -> L6 Logging, Replay, and Evaluation
```

### 4.2 L1 Acquisition

L1 admits physical or digital source signals into the pipeline with reliable timing and source provenance. The acquisition goal is capture without interpretation so downstream layers receive consistent input.

#### 4.2.1 Responsibilities

Acquisition responsibilities below define what makes intake dependable under real-time and mixed-modality conditions. The emphasis is completeness and non-blocking behavior.

- ingest raw streams from audio, video, and environmental sensors,
- attach source identifiers and timing metadata,
- buffer non-blocking input for downstream handling.

#### 4.2.2 Output Contract

The acquisition output contract below defines what must be emitted so normalization can proceed deterministically. It emphasizes source traceability and timing fidelity over semantic meaning.

- source-local event frames, minimally wrapped with source and timing metadata.

### 4.3 L2 Normalization

L2 transforms modality-specific raw inputs into canonical event forms. Normalization reduces interface complexity while preserving enough original context for auditing and fallback behavior.

#### 4.3.1 Responsibilities

Normalization responsibilities below define transformation goals. The emphasis is consistent data shape, explicit type labels, and preserved references to raw input when needed.

- convert modality-specific raw input into canonical event objects,
- preserve references to raw payloads where needed,
- classify event type and quality indicators.

#### 4.3.2 Output Contract

The normalization output contract below defines packet quality required by downstream coherence logic. Outputs must be structurally stable enough that cross-modal processing can stay generic rather than sensor-specific.

- modality-normalized event packets with stable field names and data types.

### 4.4 L3 Coherence and Integration (Pre-Semantics)

L3 turns independent normalized streams into coherent room state before interpretation. The layer resolves temporal, spatial, and evidentiary mismatch so semantics does not carry sensor reconciliation burden.

#### 4.4.1 Responsibilities

Coherence responsibilities below describe how to build decision-ready state from multiple inputs. The layer must reconcile disagreement and uncertainty while preserving provenance.

- align asynchronous streams in a shared time window,
- register events into a shared room coordinate frame,
- reconcile conflicting or duplicate observations,
- compute confidence and coherence scores,
- produce a unified room-state snapshot for semantics.

#### 4.4.2 Required Generalized Functions

Required generalized functions below operationalize coherence. They are reusable capabilities that should remain stable across sensor-specific implementations.

- temporal alignment engine,
- spatial registration map,
- cross-modal correlation rules,
- conflict-resolution policy,
- world-state assembly function.

#### 4.4.3 Output Contract

The coherence output contract below defines the handoff semantics consumes. It should carry integrated context, confidence, and traceability rather than raw event fragments.

- coherent state objects suitable for interpretation, not raw modality fragments.

### 4.5 L4 Semantics and Decisioning

L4 interprets coherent room state into decisions and intents. Semantics focuses on meaning and policy because coherence has already handled multi-source reconciliation.

#### 4.5.1 Responsibilities

Semantics responsibilities below define the decision process. Deterministic policy checks should run before higher-level interpretation in a controlled, testable order.

- interpret coherent room-state snapshots,
- apply deterministic rules and policy gates first,
- apply higher-order semantic interpretation where required,
- produce explicit state decisions and action intents.

#### 4.5.2 Scope Boundary Note

The note below marks the semantics boundary in this general specification. Detailed decision logic, ontology, and model behavior are intentionally deferred to the dedicated semantics document.

- this layer is defined here only at framework level; full decision logic belongs in a dedicated Semantics and Decisioning specification.

### 4.6 L5 Orchestration and Output Dispatch

L5 converts abstract decisions into executable actions across output systems. Orchestration is responsible for safe, prioritized, and traceable command delivery.

#### 4.6.1 Responsibilities

Orchestration responsibilities below define reliable execution behavior. The focus is translating intent into channel-specific actions without losing policy constraints.

- map action intents to output channels (audio, projection, control systems),
- enforce safety, priority, and fallback behavior,
- emit dispatch records for traceability.

#### 4.6.2 Scope Boundary Note

The note below defines where this document stops in output detail. Channel-specific cueing and system integration specifications are managed in dedicated output-stage documents.

- detailed output mappings and output-stage component specs are separate documents.

### 4.7 L6 Logging, Replay, and Evaluation

L6 provides feedback infrastructure for debugging, evaluation, and iterative refinement. Logging and replay are treated as core pipeline capabilities, not optional tooling.

#### 4.7.1 Responsibilities

Logging and evaluation responsibilities below define minimum observability required for improvement over time. These functions enable diagnosis, reproducibility, and quality tracking.

- store layer transitions and key decisions,
- support replay for debugging and comparative evaluation,
- expose quality metrics for system iteration.

## 5. Shared Data Contracts

Shared data contracts below define generalized fields that persist across layer boundaries. These contracts keep cross-layer behavior auditable, testable, and maintainable as components evolve.

### 5.1 Required Cross-Layer Fields

The field set below is the minimal cross-layer schema needed for end-to-end traceability and interpretation. It is intentionally compact so modalities can adopt it uniformly.

- `event_id` or `state_id`,
- `source_id` or integrated source set,
- `timestamp` and processing-stage timestamps,
- `spatial_context` where applicable,
- `confidence` and quality markers,
- payload or state body appropriate to that layer.

## 6. Coherence and Integration Framework (Generalized)

The framework below expands coherence into a reusable pre-semantics integration method. It defines how to evaluate evidence quality and produce unified state stable enough for decisioning.

### 6.1 Core Questions

Core questions below are gating checks the coherence layer must answer before forwarding state to semantics. They establish validity and consistency requirements.

- are observations time-compatible,
- are observations spatially compatible,
- do observations support or contradict each other,
- is confidence sufficient for semantics,
- what unified state should be advanced.

### 6.2 Generalized Processing Sequence

The sequence below is the minimal procedural flow for coherence operations. It is designed to be explicit, testable, and reusable across multiple sensor combinations.

1. Window and align incoming normalized events.
2. Register all candidate events in shared spatial context.
3. Correlate by event class and temporal overlap.
4. Resolve contradictions using policy and confidence.
5. Emit one coherent room-state object plus provenance.

## 7. Relationship to Sensor Intake Phase 1

This relationship describes how the current audio-first sensor intake specification functions as the first concrete instantiation of the generalized model. The objective is alignment, not duplication.

### 7.1 Test Case Position

The test-case position below formally places the current sensor intake document in the spec stack. It anchors implementation learning while preserving this document as the generalized reference.

The current sensor intake document should be treated as **Test Case 01 (Audio-first)** against this pipeline.

### 7.2 Mapping Rules

Mapping rules below partition responsibilities between the generalized model and the test-case specification. The partition prevents scope bleed and keeps architectural boundaries clear.

- capture and normalization details map to L1 and L2,
- cross-stream reconciliation should move under L3 conventions,
- semantics in the intake document should remain high-level and expand in the dedicated semantics spec.

## 8. Required Follow-on Specifications

The queue below defines specialized documents needed to complete the full computational specification set. The order follows dependency flow from input modalities toward interpretation and output execution.

### 8.1 Priority Specification Queue

The priority list below is the near-term authoring queue in implementation-relevant order. Completing it provides a full chain from modality-specific intake to output-stage behavior.

1. Sensor Intake: Audio Test Case 01 (existing, to be aligned)
2. Sensor Intake: Thermal Test Case
3. Sensor Intake: mmWave/Presence Test Case
4. Sensor Intake: Vision/Camera Test Case
5. Coherence and Integration Detailed Specification
6. Semantics and Decisioning Detailed Specification
7. Output Stage Detailed Specifications (audio, video, control integration)

## 9. Acceptance Criteria for This General Spec

Acceptance criteria below provide objective checks for structural completeness of the generalized document. They determine whether the team can proceed to detailed component authoring without architectural ambiguity.

### 9.1 Completion Checks

Mandatory checks below determine whether this document can be accepted as the active generalized computational reference.

- layer boundaries are explicit and non-overlapping,
- coherence/integration is defined as pre-semantics,
- sensor-specific docs can map to this model without redefining architecture,
- semantics and output details are acknowledged but deferred to dedicated docs.
