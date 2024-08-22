import os
import wave
import json
from utils import messages, recordings
from vosk import Model, KaldiRecognizer


file_path = os.path.join(os.path.dirname(__file__), "output.wav")

model = Model(model_name="vosk-model-en-us-0.22")
rec = KaldiRecognizer(model, 16000)
rec.SetWords(True)

def speech_recognition():
    with wave.open(file_path, "rb") as wf:
        if wf.getnchannels() != 1:
            raise ValueError("Audio file must be mono")

        if wf.getframerate() != 16000:
            raise ValueError("Sample rate of the audio file must be 16000")
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
            else:
                partial_result = rec.PartialResult()

    final_result = rec.FinalResult()
    print(json.loads(final_result)["text"])
    print("Transcription finished.")

if __name__ == "__main__":
    speech_recognition()
