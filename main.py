import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Initialize PyAudio
p = pyaudio.PyAudio()

# Set audio stream parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048  # Increased chunk size

# Initialize the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Initialize Matplotlib plot
plt.ion()
fig, ax = plt.subplots()

try:
    # Loop to continuously get data
    while True:
        # Read audio stream and handle overflow
        try:
            audio_data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        except IOError:
            continue  # Skip this iteration due to overflow

        # Calculate FFT and update the plot
        Pxx, freqs, bins, im = ax.specgram(audio_data, NFFT=1024, Fs=RATE, noverlap=512, scale='dB')
        plt.pause(0.001)
        ax.clear()

except KeyboardInterrupt:
    # Stop and close the audio stream and plot
    stream.stop_stream()
    stream.close()
    p.terminate()
    plt.close('all')
