"""Script that handles speech recognition on the audio file"""
import speech_recognition as sr
from pathlib import Path
import os
import numpy as np
from tqdm import tqdm
from tempfile import TemporaryDirectory

from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence, detect_nonsilent

TEMP_DIRECTORY = TemporaryDirectory()
TEMP_PATH = TEMP_DIRECTORY.name
Path(f"{TEMP_PATH}/audio-chunks").mkdir(parents=True, exist_ok=True)

RECOGNIZER = sr.Recognizer()
BASE_PATH_INTERVALS = "generated_data/speech/intervals"
BASE_PATH_TRANSCRIPTS = "generated_data/speech/transcripts"
Path(BASE_PATH_INTERVALS).mkdir(parents=True, exist_ok=True)
Path(BASE_PATH_TRANSCRIPTS).mkdir(parents=True, exist_ok=True)



def generate_large_audio_transcription(path: str):
    sound = AudioSegment.from_wav(path)

    print("INFO: Splitting audio into chunks")
    chunks, intervals = split_on_silence(sound,
                                         min_silence_len=500,
                                         silence_thresh=sound.dBFS - 14,
                                         keep_silence=500,
                                         )
    print("INFO: Audio splitting performed successfully")

    transcript_chunks = []

    print("INFO: Performing speech recognition. Progress:")
    for chunk_number, audio_chunk in tqdm(list(enumerate(chunks, start=1))):
        chunk_filename = f"{TEMP_PATH}/audio-chunks/chunk{chunk_number}.wav"
        audio_chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_listened = RECOGNIZER.record(source)
            try:
                text = RECOGNIZER.recognize_google(audio_listened, language="es-MX")
            except sr.UnknownValueError as e:
                pass
            else:
                text = f"{text.capitalize()}. "
                print("prueba", text)
                transcript_chunks.append(text)

    return transcript_chunks, intervals


def get_large_audio_transcription(path: str, ignore: bool = False) -> tuple:
    """Creates a full transcription by chunks of an audio."""
    audio_name = path.split("/")[-1].split(".")[0]

    # expected file names
    intervals_path = f"{BASE_PATH_INTERVALS}/{audio_name}.npy"
    transcript_path = f"{BASE_PATH_TRANSCRIPTS}/{audio_name}.txt"

    # Splitting audio into chunks and apply speech recognition
    if os.path.exists(intervals_path) and os.path.exists(transcript_path) and not ignore:
        print("INFO: Previously generated speech files found.")
        intervals = np.load(intervals_path)
        f = open(transcript_path, "r", encoding="utf-8")
        transcript = f.read().lower()
        f.close()
        transcript = transcript.split("\n")
        print("INFO: Finished loading speech files.")
    else:
        print("INFO: Starting speech recognition")
        transcript_chunks, intervals = generate_large_audio_transcription(path)
        np.save(intervals_path, intervals)
        transcript = ""
        for chunk in transcript_chunks:
            transcript += chunk.lower() + "\n"
        f = open(transcript_path, "w", encoding="utf-8")
        f.write(transcript)
        f.close()

    return transcript, intervals

