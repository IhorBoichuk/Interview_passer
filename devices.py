# Install pyaudio from http://people.csail.mit.edu/hubert/pyaudio/
# Find audio device index using this code
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

p.terminate()