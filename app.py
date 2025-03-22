from flask import Flask, request, jsonify, send_from_directory
import numpy as np
from scipy.io.wavfile import write
import librosa
import os

app = Flask(__name__)

# Load sound samples
sounds = {
    "kick": librosa.load("samples/kick.wav", sr=None)[0],
    "snare": librosa.load("samples/snare.wav", sr=None)[0],
    "hihat": librosa.load("samples/hihat.wav", sr=None)[0],
}

@app.route("/generate", methods=["POST"])
def generate_beatbox():
    data = request.json
    pattern = data["pattern"]  # e.g., ["kick", "snare", "hihat"]
    tempo = data["tempo"]  # e.g., 120 BPM

    # Generate beatbox audio
    beatbox_audio = generate_audio(pattern, tempo)

    # Save and return the audio file
    write("output_beatbox.wav", 44100, beatbox_audio)
    return jsonify({"audio_url": "/output_beatbox.wav"})

def generate_audio(pattern, tempo):
    # Combine sounds based on the pattern
    beat_duration = 60 / tempo  # Duration of one beat in seconds
    beat_samples = int(beat_duration * 44100)  # Convert to samples
    beatbox_audio = np.array([])

    for sound in pattern:
        sound_audio = sounds[sound]
        beatbox_audio = np.concatenate([beatbox_audio, sound_audio[:beat_samples]])

    return beatbox_audio

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    app.run(debug=True)