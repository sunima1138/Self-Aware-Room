import sounddevice as sd

print("Available audio devices:\n")
for i, device in enumerate(sd.query_devices()):
    if device["max_input_channels"] > 0:
        print(f"  [{i}] {device['name']}  (channels: {device['max_input_channels']})")

print(f"\nYour default input device: {sd.query_devices(kind='input')['name']}")
