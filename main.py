"""Main script for the comedy processor."""
from algorithms.audio_process.speech import process_speech
from algorithms.audio_process.visualizer import generate_graphics
from interphase.player import start_ui

if __name__ == "__main__":
    audio = "input_data/audios/loteria_2.wav"
    script = "input_data/scripts/loteria_2.txt"
    speech_output = process_speech(audio, script)
    graphic = generate_graphics(audio)
    start_ui(speech_output, graphic)
