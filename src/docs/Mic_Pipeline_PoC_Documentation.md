# Microphone-to-Pipeline PoC — Documentation

**Author:** Suni Dangol
**Location:** src/mic_poc.py
**Repo:** https://github.com/sunima1138/Self-Aware-Room (personal fork of CHI-CityTech/Self-Aware-Room)
**Branch:** main
**Commit:** c9b6018 — "feat: single-file mic-to-pipeline PoC with speech-to-text"
**Direct link:** https://github.com/sunima1138/Self-Aware-Room/blob/main/src/mic_poc.py

## What this is

A working proof of concept that takes real microphone input, converts it to text using a local speech-to-text model, and passes that text through 7 logged pipeline stages (matching the SAR general spec's L1-L5B layers), ending in a printed confirmation of what was said.

This is not one of the 4 assigned GitHub issues -- it's an extra, self-directed PoC built to prove the pipeline concept works with real audio input.

## How it works

1. L1 Acquisition -- records 5 seconds of audio from the default microphone (sounddevice), then transcribes it to text using a local Whisper model (faster-whisper, tiny.en, runs on CPU).
2. L2 Normalization -- trims whitespace from the transcribed text.
3. L3 Coherence -- stub (single sensor, nothing to fuse yet).
4. L4A Semantic -- stub (real interpretation logic comes later).
5. L4B Decision -- stub (real decision logic comes later).
6. L5A Orchestration -- stub.
7. L5B Dispatch -- prints "A user said: '<transcribed text>'" to console.

Every stage logs its own pass to a shared Logger object, tagged with the same trace_id, so the code verifies all 7 stages actually fired before declaring success.

## How to run it

    cd src
    source ../.venv/bin/activate
    python3 mic_poc.py

## Verified result (real run)

Spoke into the microphone; the script correctly transcribed the audio and confirmed all 7 stages fired under a single shared trace_id, ending in the console printing what was said back out.

## Libraries used

- sounddevice -- microphone capture
- faster-whisper -- local speech-to-text

## Next steps

- Split this single file into the multi-file sar_pipeline/ package structure for issue #2.
- Replace the L4A stub with real semantic interpretation logic.
- Open a Pull Request from this fork back to CHI-CityTech/Self-Aware-Room.