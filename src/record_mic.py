import sounddevice as sd
import numpy as np
from datetime import datetime, timezone

SAMPLE_RATE = 16000
DURATION_SECONDS = 5
CHUNK_SECONDS = 1


def record_audio(duration, sample_rate):
    print(f"Recording for {duration} seconds... speak now.")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate,
                    channels=1, dtype="float32")
    sd.wait()
    print("Done recording.")
    return audio.flatten()


def to_records(audio, sample_rate, chunk_seconds):
    chunk_size = sample_rate * chunk_seconds
    records = []
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i + chunk_size]
        volume = float(np.abs(chunk).mean())
        record = {
            "device_id": "MIC_01",
            "data_type": "audio_chunk",
            "source_timestamp": datetime.now(timezone.utc).isoformat(),
            "sample_rate": sample_rate,
            "num_samples": len(chunk),
            "mean_volume": round(volume, 5),
        }
        records.append(record)
    return records


if __name__ == "__main__":
    audio = record_audio(DURATION_SECONDS, SAMPLE_RATE)
    records = to_records(audio, SAMPLE_RATE, CHUNK_SECONDS)

    print(f"\nCreated {len(records)} data records:\n")
    for r in records:
        print(r)
