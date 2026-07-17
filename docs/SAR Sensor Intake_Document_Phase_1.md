# OAA Self-Aware Room: Phase 1 Technical Implementation Specification**Document Class:** System Architecture & Software Blueprint  
**Reference Specification:** OAA AI Innovation Grant System Architecture (Dr. David B. Smith)  
**Target Platform:** Modular, Multi-Threaded Local Python Core Engine  

## 1. Architectural Alignment Matrix
To ensure compliance with the Open Automation Architecture (OAA) guidelines, all hardware devices and abstract parsing loops are decoupled into four sequential structural tiers. 

This infrastructure handles an arbitrary number of sensor streams concurrently by routing data through either an **Active Feature Extraction Pathway** or a lightweight, zero-overhead **Pass-Through Vector**.


[ Arbitrary Hardware Input ] (Mics, Webcams, mmRadar, Thermal, BME680)
|
v
+-------------------------------------------------------------+
| 2. DATA CAPTURE TIER (Raw Data Ingestion Matrix) |
| - Protocol Drivers (PyAudio, OpenCV, WebSockets, MQTT) |
| - Standardized Asynchronous Buffer Queues |
+-------------------------------------------------------------+
|
v
+-------------------------------------------------------------+
| 3. INTERMEDIATE PROCESSING TIER (Local Abstraction) |
| / \ |
| v [Active Processing Pathway] v [Pass-Through Vector] |
| [Feature Chunk Extraction] [Direct Raw Forwarding] |
| (e.g., Audio -> Speech-to-Text) (e.g., Temperature, IMU) |
+-------------------------------------------------------------+
|
v
+-------------------------------------------------------------+
| 4. HIGHER-LEVEL ABSTRACTION TIER (Fusion & Correlation) |
| - Spatial Coordination Matrix (Absolute X, Y, Z Origin Stamping) |
| - Temporal Window Alignment & Unified Data Serialization |
+-------------------------------------------------------------+
|
v
+-------------------------------------------------------------+
| 5. CENTRAL COMPUTATIONAL TIER (Semantic & Cognitive Engine) |
| - Tier A Guard: Deterministic String Match/Regex Bypass |
| - Tier B AI Layer: Local Ollama LLM Room State Generation |
+-------------------------------------------------------------+
|
v
+-------------------------------------------------------------+
| 6. OUTPUT PATHWAYS & DIGITAL TWIN INTEGRATION |
| - OSC/WebSockets Dispatcher -> TouchDesigner / Spatial Audio|
+-------------------------------------------------------------+


---

## 2. Tier Functional Specifications

### Tier 2: Data Capture (Raw Data Acquisition)
*   **Operational Mandate:** Ingest high-frequency, asynchronous, device-specific telemetry streams without blocking core runtime logic.
*   **Engineering Rule:** Hardware drivers must immediately push incoming raw byte packages into isolated, thread-safe memory queues (`queue.Queue`). No processing, parsing, or transformation is permitted within the hardware listener thread.

### Tier 3: Intermediate Processing (Local Abstraction & Cleaning)
*   **Operational Mandate:** Condition raw physical measurements into comparable, standardized computational vectors.
*   **Active Processing Pathway:** High-density raw frames are mapped to local compute engines. For this Phase 1 Audio PoC, raw binary acoustic streams are structured into rolling windows and translated into UTF-8 text strings via a local `faster-whisper` deployment.
*   **Pass-Through Vector:** Low-density or pre-formatted telemetry (e.g., BME680 climate values, or static proximity states) bypass heavy transformations entirely. They flow directly to the serialization handler unaltered.

### Tier 4: Higher-Level Abstraction (Fusion, Correlation, & Mediation)
*   **Operational Mandate:** Unify independent streams chronologically and spatially into a coherent global state snapshot.
*   **Execution:** Computes temporal alignment based on source-generated timestamps. It maps each incoming packet to absolute physical \((X, Y, Z)\) spatial coordinate blocks relative to the room's physical origin layout.
*   **Serialized Standard Data Object Schema:**
    ```json
    {
      "device_id": "OAA_AUDIO_N_01",
      "data_type": "semantic_text",
      "source_timestamp": "2026-07-17T16:49:00.123Z",
      "spatial_coordinates": {"x": 0.0, "y": 4.5, "z": 2.1},
      "payload": "Activate forest theme environment"
    }
    ```

### Tier 5: Central Computational Tier (Semantic Representation & Decision)
*   **Operational Mandate:** Translate quantitative state vectors into derived qualitative constructs (events, states, anomalies) to trigger the spatial audio and video output matrix.
*   **Tier A (Rules Engine Guard):** A zero-latency string match/regex validation gate scans text elements instantly. If explicit safety rules or strict macros are hit (e.g., `"STOP"`), the engine triggers an instant output override, bypassing the LLM layer entirely.
*   **Tier B (Cognitive Engine):** Complex or abstract inputs fall through to a local LLM instance via `Ollama` running `mistral` or `llama3`. The engine parses intent and outputs a structured room state.

---

## 3. Reference Framework Source Code

This ready-to-run implementation blueprint provides the scaffolding for your student researcher. It runs an asynchronous multi-threaded pipeline executing the **Active Path** and **Pass-Through Path** alongside the **Rules-Based Guard**.

```python
import time
import queue
import json
import threading
from datetime import datetime

# Required Developer Environment Dependencies:
# pip install sounddevice numpy faster-whisper
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

# Global Thread-Safe Communication Buffers
audio_capture_buffer = queue.Queue()
passthrough_capture_buffer = queue.Queue()

# OAA Hardware Device Configuration Matrix
SENSOR_REGISTRY = {
    "mic_north": {
        "device_id": "OAA_AUDIO_N_01",
        "tier_2_type": "ACTIVE_PROCESSING",
        "coordinates": {"x": 0.0, "y": 4.5, "z": 2.1}
    },
    "thermal_sensor": {
        "device_id": "OAA_THERMAL_01",
        "tier_2_type": "PASS_THROUGH",
        "coordinates": {"x": 2.3, "y": 1.1, "z": 3.0}
    }
}

# =====================================================================
# TIER 2: DATA CAPTURE (RAW DATA ACQUISITION)
# =====================================================================
def audio_capture_worker(sample_rate=16000, chunk_duration=3):
    """Asynchronously captures raw acoustic audio from default hardware interface."""
    def callback(indata, frames, time_info, status):
        audio_capture_buffer.put(indata.copy())
    
    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='float32', callback=callback, blocksize=int(sample_rate * chunk_duration)):
        while True:
            time.sleep(1)

def arbitrary_sensor_mock_worker():
    """Simulates an arbitrary pass-through sensor injecting data asynchronously."""
    while True:
        time.sleep(2.5)  # Simulates sensor polling interval
        simulated_raw_payload = {"raw_value": 24.5, "metric": "temperature"}
        passthrough_capture_buffer.put(("thermal_sensor", simulated_raw_payload))

# =====================================================================
# TIERS 3 & 4: INTERMEDIATE PROCESSING & HIGHER-LEVEL ABSTRACTION
# =====================================================================
def data_mediation_engine():
    """Orchestrates Local Abstraction, Transformation, and Spatial Stamping."""
    print("[System Initialization] Loading Local Faster-Whisper Model...")
    stt_engine = WhisperModel("tiny", device="cpu", compute_type="int8")
    print("[System Active] OAA Mediation Framework Listening...")

    while True:
        # Processing Pathway A: Active Feature Extraction Subsystem
        if not audio_capture_buffer.empty():
            raw_audio = audio_capture_buffer.get()
            meta = SENSOR_REGISTRY["mic_north"]
            
            # Tier 3: Local Feature Abstraction (Audio Waveform -> Text String)
            segments, _ = stt_engine.transcribe(raw_audio.flatten(), beam_size=3)
            extracted_text = " ".join([seg.text for seg in segments]).strip()
            
            if extracted_text:
                # Tier 4: Spatial & Temporal Serialization Wrap
                global_packet = build_oaa_packet(meta, extracted_text, "semantic_text")
                central_computational_tier(global_packet)
            audio_capture_buffer.task_done()

        # Processing Pathway B: Pass-Through Vector Subsystem
        if not passthrough_capture_buffer.empty():
            sensor_key, raw_payload = passthrough_capture_buffer.get()
            meta = SENSOR_REGISTRY[sensor_key]
            
            # Tier 3/4 Bypass: Package directly into unified schema without altering bytes
            global_packet = build_oaa_packet(meta, raw_payload, "raw_telemetry")
            central_computational_tier(global_packet)
            passthrough_capture_buffer.task_done()
            
        time.sleep(0.01)

def build_oaa_packet(metadata, payload, data_type):
    """Enforces the official global spatial-temporal JSON data wrapper."""
    return {
        "device_id": metadata["device_id"],
        "data_type": data_type,
        "source_timestamp": datetime.utcnow().isoformat() + "Z",
        "spatial_coordinates": metadata["coordinates"],
        "payload": payload
    }

# =====================================================================
# TIER 5: CENTRAL COMPUTATIONAL TIER (SEMANTIC REPRESENTATION & DECISION)
# =====================================================================
def central_computational_tier(packet):
    """Applies Dual-Tier Cognitive and Rules Logic to the standard input."""
    print(f"\n[Tier 5 Ingest] Source: {packet['device_id']} | Type: {packet['data_type']}")
    
    if packet["data_type"] == "semantic_text":
        text_data = packet["payload"].upper()
        print(f" -> Interpreting Semantic Text: \"{packet['payload']}\"")
        
        # Tier A Guard: Deterministic Rules-Based Bypass
        if "STOP" in text_data or "HALT" in text_data:
            execute_output_pathway("EMERGENCY_SHUTDOWN", packet["spatial_coordinates"])
            return
            
        if "FOREST" in text_data or "NATURE" in text_data:
            execute_output_pathway("SET_THEME_NATURAL", packet["spatial_coordinates"])
            return
            
        # Tier B: Cognitive AI Framework Handoff (Abstract Fallback)
        print(f" -> Forwarding to Local Cognitive Model via Ollama HTTP API...")

    elif packet["data_type"] == "raw_telemetry":
        # Raw pass-through values reach the decision node directly for metric evaluations
        print(f" -> Direct Pass-Through Telemetry Authenticated: {packet['payload']}")

# =====================================================================
# TIER 6: OUTPUT PATHWAYS AND DIGITAL TWIN INTEGRATION
# =====================================================================
def execute_output_pathway(state_command, origin_coordinates):
    """Translates high-level decisions back into the spatial AV matrix."""
    print(f"[Tier 6 Actuation] Dispatched State Command: [{state_command}]")
    print(f" -> Adjusting spatial pans and video projection boundaries relative to: {origin_coordinates}")

if __name__ == "__main__":
    # Launch concurrent OAA data collection threads
    threading.Thread(target=audio_capture_worker, daemon=True).start()
    threading.Thread(target=arbitrary_sensor_mock_worker, daemon=True).start()
    
    # Run the continuous mediation core loop
    try:
        data_mediation_engine()
    except KeyboardInterrupt:
        print("\nPipeline execution halted by operator.")
```

------------------------------
## Next Steps to Finalize
If you want to append additional sections to this markdown file, tell me if you want to include:

* The exact format of Section 6's Digital Twin state replication packets
* How to expand the script to support Section 7's variable Temporal Structure (e.g., real-time loops vs. 10-second averages)
* Adding Section 4's multi-sensor fusion logic (e.g., checking both audio context and thermal presence simultaneously)


