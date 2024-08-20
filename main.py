from flask import Flask, render_template, request, jsonify
from threading import Thread
from record import messages, recordings

from record import record_speakers
from voicetotextmodel import speech_recognition

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_recording():
    messages.put(True)
    
    def record_thread():
        record_speakers()
        
    def transcribe_thread():
        speech_recognition()
    
    record = Thread(target=record_thread)
    record.start()
    
    transcribe = Thread(target=transcribe_thread)
    transcribe.start()

    return jsonify({"status": "Recording started"}), 200

@app.route('/stop', methods=['POST'])
def stop_recording():
    if not messages.empty():
        messages.get()

    return jsonify({"status": "Recording stopped"}), 200

if __name__ == '__main__':
    app.run(debug=True)
