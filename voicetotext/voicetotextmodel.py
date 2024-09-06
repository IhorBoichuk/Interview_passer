import os
import wave
import json
from vosk import Model, KaldiRecognizer
import socket

HOST = '0.0.0.0'  # Слухає на всіх доступних IP
PORT = 8002      # Порт для прослуховування
BUFFER_SIZE = 1024  # Розмір буфера для прийому даних

# Ініціалізація моделі для розпізнавання мови
model = Model(model_name="vosk-model-en-us-0.22")
rec = KaldiRecognizer(model, 16000)
rec.SetWords(True)

def handle_client(conn, addr):
    """Функція для обробки клієнтського з'єднання."""
    print(f'Connected by {addr}')
    results = []
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break  # Якщо даних немає, завершуємо з'єднання

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                results.append(result["text"])
                print(f"Final Result: {result['text']}")
            else:
                partial_result = json.loads(rec.PartialResult())
                print(f"Partial Result: {partial_result['partial']}")

        final_result = json.loads(rec.FinalResult())
        results.append(final_result["text"])
        print(f"Final transcription: {' '.join(results)}")
    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        conn.close()
        print("Connection closed")

def speech_recognition_server():
    """Функція для запуску сервера розпізнавання мови."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

