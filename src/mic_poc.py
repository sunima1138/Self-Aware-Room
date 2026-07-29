"""
Self-Aware Room -- Microphone Pipeline PoC (fruit detection -> TouchDesigner)
Speak into the mic -> text -> passes through 7 logged stages -> if a fruit
word is detected, sends its number (1-5) to TouchDesigner via OSC.

Network settings follow SAR_Network_and_OSC_Communications_Experiment_v0.1:
dedicated Ethernet, Windows/TouchDesigner static IP 192.168.50.20, port 9000.
"""

# generates unique random IDs (for trace_id)
import uuid
# lets Python record audio from the microphone
import sounddevice as sd
# for timestamping each Observation
from datetime import datetime, timezone
# the local speech-to-text model
from faster_whisper import WhisperModel
# sends network messages to TouchDesigner (OSC protocol)
from pythonosc.udp_client import SimpleUDPClient

# audio samples captured per second -- 16kHz is standard for speech
SAMPLE_RATE = 16000
DURATION_SECONDS = 5      # how many seconds to record each time we listen

# --- TouchDesigner networking setup (per team protocol doc) ---
# Windows PC's static Ethernet IP (from the team's network doc)
TOUCHDESIGNER_IP = "192.168.50.20"
# must match the port set on TouchDesigner's OSC In DAT
TOUCHDESIGNER_PORT = 9000
# reusable "connection" object we can send() through
osc = SimpleUDPClient(TOUCHDESIGNER_IP, TOUCHDESIGNER_PORT)

# --- fruit -> number mapping ---
# A dictionary is a lookup table: word on the left, number on the right.
# Multiple words can point to the same number (misspellings, singular/plural).
FRUIT_NUMBERS = {
    "blueberry": 1,
    "strawberry": 2,
    "apple": 3,
    "banana": 4,
    "bannana": 4,   # common misspelling, mapped to the same number as "banana"
    "grapes": 5,
    "grape": 5,     # singular form, same number as "grapes"
}


def detect_fruit(text: str):
    """Scans transcribed text for any known fruit word.
    Returns (fruit_word, number) if found, or (None, None) if not."""
    lowered = text.lower()  # lowercase everything so "Apple" and "apple" both match
    for fruit_word, number in FRUIT_NUMBERS.items():  # loop through every word->number pair
        if fruit_word in lowered:   # check if this fruit word appears anywhere in the sentence
            return fruit_word, number  # stop and return as soon as we find one match
    return None, None  # ran through the whole dictionary, found nothing


# ---------- the "Observation" that travels through every stage ----------

class Observation:
    """The single object that gets passed from stage to stage.
    Every pipeline function receives one of these and (optionally)
    attaches new information to it before passing it along."""

    def __init__(self, device_id, data_type, payload):
        # __init__ runs automatically whenever a new Observation is created
        # random unique ID, shortened to 8 characters
        self.trace_id = str(uuid.uuid4())[:8]
        # which sensor produced this (e.g. "MIC_01")
        self.device_id = device_id
        # what kind of data this is (e.g. "speech_text")
        self.data_type = data_type
        # the actual content -- in our case, the spoken text
        self.payload = payload
        # when this Observation was created
        self.timestamp = datetime.now(timezone.utc)


# ---------- the logger every stage reports to ----------

class Logger:
    """Keeps a record of every pipeline stage that has run, so we can
    prove afterward that no stage was silently skipped."""

    def __init__(self):
        self.events = []  # empty list -- will fill up with stage names as they log in

    def log(self, level_name, trace_id, message):
        """Called by every stage when it finishes its work."""
        self.events.append(level_name)  # record that this stage ran
        # print a formatted line so you can watch the pipeline execute live
        print(f"[LOG] {level_name:<20} | trace={trace_id} | {message}")

    def verify(self, expected_levels):
        """Checks that every stage we expected to run actually did.
        Returns a list of any stage names that never logged in (should be empty if all is well)."""
        missing = [lvl for lvl in expected_levels if lvl not in self.events]
        return missing


# ---------- L1: microphone + speech-to-text ----------

def l1_acquisition(logger):
    """The only stage that touches the real, physical world --
    everything after this works with the text it produces."""
    print(f"\nListening for {DURATION_SECONDS} seconds... speak now.")

    # sd.rec() starts recording; first argument is total number of samples
    # (seconds * samples-per-second); channels=1 means mono (one microphone)
    audio = sd.rec(int(DURATION_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                   channels=1, dtype="float32")
    sd.wait()  # pause here until the recording actually finishes
    print("Transcribing...")

    # Load the speech-to-text model. "tiny.en" = smallest/fastest English-only version.
    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

    # .flatten() reshapes the audio into what the model expects.
    # The model returns "segments" -- chunks of recognized speech.
    segments, _ = model.transcribe(audio.flatten(), language="en")

    # Join all the segments into one clean string, trimming extra whitespace from each piece.
    text = " ".join(seg.text.strip() for seg in segments).strip()

    if not text:  # fallback in case nothing was understood
        text = "(nothing understood)"

    # Wrap the result in an Observation -- the standard object every stage expects
    obs = Observation(device_id="MIC_01",
                      data_type="speech_text", payload=text)
    logger.log("L1 Acquisition", obs.trace_id,
               f"captured and transcribed: {text!r}")
    return obs


# ---------- L2 through L5B: simple stages, each logs and passes through ----------

def l2_normalization(obs, logger):
    """Cleans up the raw text. Currently just trims whitespace --
    this is where more cleanup logic would go later."""
    obs.payload = obs.payload.strip()
    logger.log("L2 Normalization", obs.trace_id, "normalized text")
    return obs


def l3_coherence(obs, logger):
    """Placeholder for cross-sensor fusion. With only one sensor (the mic),
    there's nothing to fuse yet -- this stage does nothing but log."""
    logger.log("L3 Coherence", obs.trace_id,
               "checked coherence (single source)")
    return obs


def l4a_semantic(obs, logger):
    """The real interpretation logic: figures out what the text MEANS.
    Here, that means checking whether a fruit word was mentioned."""
    fruit_word, number = detect_fruit(obs.payload)

    if fruit_word:
        logger.log("L4A Semantic", obs.trace_id,
                   f"detected fruit: {fruit_word!r} -> {number}")
    else:
        logger.log("L4A Semantic", obs.trace_id, "no known fruit detected")

    # Attach the results directly onto the Observation so later stages can use them
    obs.fruit_word = fruit_word
    obs.fruit_number = number
    return obs


def l4b_decision(obs, logger):
    """Decides what to do based on what L4A found.
    Doesn't actually send anything yet -- just records the decision."""
    if obs.fruit_number is not None:
        logger.log("L4B Decision", obs.trace_id,
                   "decided: send fruit number to TouchDesigner")
    else:
        logger.log("L4B Decision", obs.trace_id,
                   "decided: nothing to dispatch (no fruit detected)")
    return obs


def l5a_orchestration(obs, logger):
    """Placeholder for coordinating multiple output actions.
    With only one output (TouchDesigner), there's nothing to coordinate yet."""
    logger.log("L5A Orchestration", obs.trace_id, "planned output action")
    return obs


def l5b_dispatch(obs, logger):
    """The finish line -- prints the result and sends it to TouchDesigner
    over the network, if a fruit was actually detected."""
    logger.log("L5B Dispatch", obs.trace_id,
               "dispatched to console + TouchDesigner")
    print(f"\n[OUTPUT] A user said: {obs.payload!r}\n")

    if obs.fruit_number is not None:
        # send_message(address, value) -- "address" is just a label TouchDesigner
        # uses to identify this type of message; "value" is the actual data.
        osc.send_message("/sar/fruit_number", obs.fruit_number)
        print(f"[NETWORK] Sent fruit number {obs.fruit_number} ({obs.fruit_word}) "
              f"to {TOUCHDESIGNER_IP}:{TOUCHDESIGNER_PORT}")
    else:
        # Explicitly say nothing was sent, rather than silently doing nothing --
        # makes debugging much easier later.
        print("[NETWORK] No known fruit detected -- nothing sent to TouchDesigner")

    return obs


# ---------- run everything in order ----------

def main():
    logger = Logger()

    # One Observation object gets passed through every stage in a straight line.
    # Each function can read it, change it, and hands back the (possibly updated) version.
    obs = l1_acquisition(logger)
    obs = l2_normalization(obs, logger)
    obs = l3_coherence(obs, logger)
    obs = l4a_semantic(obs, logger)
    obs = l4b_decision(obs, logger)
    obs = l5a_orchestration(obs, logger)
    obs = l5b_dispatch(obs, logger)

    # Final proof step: confirm every stage we expected actually ran.
    expected = ["L1 Acquisition", "L2 Normalization", "L3 Coherence",
                "L4A Semantic", "L4B Decision", "L5A Orchestration", "L5B Dispatch"]
    missing = logger.verify(expected)

    if missing:
        print(f"MISSING STAGES: {missing}")
    else:
        print(f"All {len(expected)} stages confirmed for trace_id={obs.trace_id}")


# This means: only run main() if this file was executed directly
# (e.g. "python3 mic_poc.py"), not if it were imported by another file.
if __name__ == "__main__":
    main()
