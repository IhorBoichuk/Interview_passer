import os
import wave
import pyaudio
from threading import Thread
from voicetotextmodel import speech_recognition
from utils import messages, recordings

CHANNELS = 1
FRAME_RATE = 16000
RECORD_SECONDS = 20
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

OUTPUT_FILENAME = "output.wav"


def record_speakers(chunk=1024):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate=FRAME_RATE,
        input=True,
        input_device_index=2,
        frames_per_buffer=chunk,
    )

    frames = []

    while not messages.empty():
        data = stream.read(chunk)
        frames.append(data)
        if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
            recordings.put(frames.copy())
            frames = []

    stream.stop_stream()
    stream.close()
    p.terminate()

    fpath = os.path.join(os.path.dirname(__file__), OUTPUT_FILENAME)
    print("Save the recorded data as a WAV file")
    with wave.open(fpath, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(AUDIO_FORMAT))
        wf.setframerate(FRAME_RATE)
        wf.writeframes(b"".join(frames))

    print(f"Recording saved to {OUTPUT_FILENAME}")
    speech_recognition()
