import tkinter as tk
from threading import Thread
from recording.record import record_speakers
from recording.utils import messages


def start_recording():
    messages.put(True)

    output_text.insert(tk.END, "Starting...\n")
    output_text.see(tk.END)

    record = Thread(target=record_speakers)
    record.start()


def stop_recording():
    if not messages.empty():
        messages.get()
    output_text.insert(tk.END, "Stopped.\n")
    output_text.see(tk.END)


root = tk.Tk()
root.title("Recording and Transcription")

record_button = tk.Button(
    root, text="Record", bg="green", fg="white", command=start_recording
)
record_button.pack(pady=10)


stop_button = tk.Button(root, text="Stop", bg="red", fg="white", command=stop_recording)
stop_button.pack(pady=10)

output_text = tk.Text(root, wrap="word", height=15, width=50)
output_text.pack(pady=10)

root.mainloop()
