"""Main script for the comedy processor."""
from algorithms.audio_process.speech import process_speech
from algorithms.audio_process.visualizer import generate_graphics
from interphase.player import start_ui

test_data = [
    {"script_joke": "jajajajjajajaja",
     "transcript_joke": "jejejejejje",
     "time_interval": [0, 10]},
    {"script_joke": "a;lskdjf;klajs;lf",
     "transcript_joke": "jejrkldlkfads",
     "time_interval": [10, 20]},
]

if __name__ == "__main__":
    audio = "input_data/audios/loteria_3.wav"
    script = "input_data/scripts/loteria_2.txt"
    list_of_jokes = process_speech(audio, script)
    graphic = generate_graphics(audio)
    app = start_ui(test_data, graphic)
    app.run(port=2000)
