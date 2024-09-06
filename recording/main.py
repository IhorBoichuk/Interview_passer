import tkinter as tk
from threading import Thread
from record import record_speakers
from utils import messages
import socket

HOST = '172.17.0.2'  # IP-адреса контейнера сервера
PORT = 65432         # Той самий порт, що й у сервера

def start_recording():
    messages.put(True)

    output_text.insert(tk.END, "Starting...\n")
    output_text.see(tk.END)

    record = Thread(target=record_speakers)
    record.start()


def stop_recording():
    if not messages.empty():
        data = messages.get()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(data)
    output_text.insert(tk.END, "Stopped.\n")
    output_text.see(tk.END)


root = tk.Tk()
root.title("Recording and Transcription")

record_button = tk.Button(
    root, text="Record", bg="green", fg="white", command=start_recording
)
record_button.pack(pady=10)

stop_button = tk.Button(
    root,
    text="Stop",
    bg="red",
    fg="white",
    command=stop_recording
    )
stop_button.pack(pady=10)

output_text = tk.Text(root, wrap="word", height=15, width=50)
output_text.pack(pady=10)

root.mainloop()
