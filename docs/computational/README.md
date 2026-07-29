# SAR Computational Document Index

This index defines sortable document identifiers for the computational specification set.

## Numbering Scheme

- `D00.xx`: Baseline and governance
- `D01.xx`: Architecture and computational pipeline
- `D02.xx`: Class, object, and implementation model
- `D03.xx`: Component and test-case intake specifications
- `D04.xx`: Implementation baseline, tooling, and delivery

Profile convention:

- `D01.02`: generalized shared streaming contract
- `D01.02.xx`: modality-specific streaming profiles

## Active Documents

| Doc ID | Section | Title | Document Link | Version/Date | Status |
| --- | --- | --- | --- | --- | --- |
| D00.02 | Baseline/Governance | SAR Computational Glossary | [Computational Glossary](D00.02_SAR_Computational_Glossary_V1_2026-07-29.md) | V1 / 2026-07-29 | Draft |
| D01.01 | Architecture | SAR General Computational Pipeline Specification | [General Computational Pipeline Spec](D01.01_SAR_General_Computational_Pipeline_Spec_V1.1_2026-07-27.md) | V1.1 / 2026-07-27 | Baseline draft |
| D01.02 | Shared Contract | SAR Shared Streaming Contract | [Shared Streaming Contract](D01.02_SAR_Shared_Streaming_Contract_V1_2026-07-29.md) | V1 / 2026-07-29 | Draft |
| D01.02.01 | Shared Contract Profile | SAR Audio Streaming Profile | [Audio Streaming Profile](D01.02.01_SAR_Audio_Streaming_Profile_V1_2026-07-29.md) | V1 / 2026-07-29 | Draft |
| D01.03 | Coherence/Correlation | SAR Coherence, Correlation, and Integration Detailed Specification | [Coherence/Correlation Detailed Spec](D01.03_SAR_Coherence_Correlation_and_Integration_Detailed_Spec_V0_2026-07-28.md) | V0 / 2026-07-28 | Stub |
| D01.04 | Runtime Identity Policy | SAR Run and Session Identity and Boundary Policy | [Run and Session Identity Policy](D01.04_SAR_Run_and_Session_Identity_and_Boundary_Policy_V1_2026-07-28.md) | V1 / 2026-07-28 | Draft |
| D02.01 | Implementation Model | SAR Computational Class and Object Model | [Class and Object Model](D02.01_SAR_Computational_Class_and_Object_Model_V1_2026-07-27.md) | V1 / 2026-07-27 | Draft |
| D03.01 | Component/Test Case | SAR Sensor Intake: Phase 1 Technical Implementation Specification | [Sensor Intake Phase 1 Spec](D03.01_SAR_Sensor_Intake_Document_Phase_1.md) | Phase 1 | Draft |
| D04.01 | Tooling/Delivery | SAR Implementation Baseline: Libraries, Tooling, and Engineering Delivery | [Implementation Baseline and Tooling](D04.01_SAR_Implementation_Baseline_Libraries_and_Tooling.md) | 2026-07-18 | Draft for build planning |
| D04.02 | Setup/Operations | SAR Computational Pipeline Setup Instructions | [Pipeline Setup Instructions](D04.02_SAR_Computational_Pipeline_Setup_Instructions_V1_2026-07-29.md) | V1 / 2026-07-29 | Draft |

## Streaming Profile Matrix (D01.02.xx)

This matrix reserves and tracks modality profiles that extend D01.02.

| Doc ID | Modality | Profile Title | Document Link | Status |
| --- | --- | --- | --- | --- |
| D01.02.01 | Audio | SAR Audio Streaming Profile | [Audio Streaming Profile](D01.02.01_SAR_Audio_Streaming_Profile_V1_2026-07-29.md) | Draft |
| D01.02.02 | Video | SAR Video Streaming Profile | Pending authoring | Planned |
| D01.02.03 | Depth/Spatial | SAR Depth and Spatial Streaming Profile | Pending authoring | Planned |
| D01.02.04 | Motion/IMU | SAR Motion and IMU Streaming Profile | Pending authoring | Planned |
| D01.02.05 | Control/Event | SAR Control and Event Streaming Profile | Pending authoring | Planned |

## Reserved IDs

- `D00.01`: [Oaa Self-aware Room - Design Specification 2026-04-27.pdf](../Oaa%20Self-aware%20Room%20%E2%80%93%20Design%20Specification%202026-04-27.pdf)

## Deprecated (Pending Archive)

- D01.02 legacy combined profile: [Legacy Combined Audio Contract (to archive)](D01.02_SAR_Shared_Data_and_Interface_Contract_Audio_Streaming_Profile_V1_2026-07-28.md)

## Reference Convention

Use both Doc ID and filename in cross-references.

Example: `D01.01 - D01.01_SAR_General_Computational_Pipeline_Spec_V1.1_2026-07-27.md`
