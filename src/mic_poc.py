"""
Self-Aware Room -- Microphone Pipeline PoC
Speak into the mic -> text -> passes through 7 logged stages -> printed output.
"""

import uuid
import sounddevice as sd
from datetime import datetime, timezone
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
DURATION_SECONDS = 5

# ---------- the "Observation" that travels through every stage ----------

class Observation:
    def __init__(self, device_id, data_type, payload):
        self.trace_id = str(uuid.uuid4())[:8]
        self.device_id = device_id
        self.data_type = data_type
        self.payload = payload
        self.timestamp = datetime.now(timezone.utc)


# ---------- the logger every stage reports to ----------

class Logger:
    def __init__(self):
        self.events = []

    def log(self, level_name, trace_id, message):
        self.events.append(level_name)
        print(f"[LOG] {level_name:<20} | trace={trace_id} | {message}")

    def verify(self, expected_levels):
        missing = [lvl for lvl in expected_levels if lvl not in self.events]
        return missing


# ---------- L1: microphone + speech-to-text ----------

def l1_acquisition(logger):
    print(f"\nListening for {DURATION_SECONDS} seconds... speak now.")
    audio = sd.rec(int(DURATION_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                    channels=1, dtype="float32")
    sd.wait()
    print("Transcribing...")

    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio.flatten(), language="en")
    text = " ".join(seg.text.strip() for seg in segments).strip()
    if not text:
        text = "(nothing understood)"

    obs = Observation(device_id="MIC_01", data_type="speech_text", payload=text)
    logger.log("L1 Acquisition", obs.trace_id, f"captured and transcribed: {text!r}")
    return obs


# ---------- L2 through L5B: simple stages, each logs and passes through ----------

def l2_normalization(obs, logger):
    obs.payload = obs.payload.strip()
    logger.log("L2 Normalization", obs.trace_id, "normalized text")
    return obs


def l3_coherence(obs, logger):
    logger.log("L3 Coherence", obs.trace_id, "checked coherence (single source)")
    return obs


def l4a_semantic(obs, logger):
    logger.log("L4A Semantic", obs.trace_id, "interpreted meaning")
    return obs


def l4b_decision(obs, logger):
    logger.log("L4B Decision", obs.trace_id, "decided: pass to output")
    return obs


def l5a_orchestration(obs, logger):
    logger.log("L5A Orchestration", obs.trace_id, "planned output action")
    return obs


def l5b_dispatch(obs, logger):
    logger.log("L5B Dispatch", obs.trace_id, "dispatched to console")
    print(f"\n[OUTPUT] A user said: {obs.payload!r}\n")
    return obs


# ---------- run everything in order ----------

def main():
    logger = Logger()
    obs = l1_acquisition(logger)
    obs = l2_normalization(obs, logger)
    obs = l3_coherence(obs, logger)
    obs = l4a_semantic(obs, logger)
    obs = l4b_decision(obs, logger)
    obs = l5a_orchestration(obs, logger)
    obs = l5b_dispatch(obs, logger)

    expected = ["L1 Acquisition", "L2 Normalization", "L3 Coherence",
                "L4A Semantic", "L4B Decision", "L5A Orchestration", "L5B Dispatch"]
    missing = logger.verify(expected)
    if missing:
        print(f"MISSING STAGES: {missing}")
    else:
        print(f"All {len(expected)} stages confirmed for trace_id={obs.trace_id}")


if __name__ == "__main__":
    main()