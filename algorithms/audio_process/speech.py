"""Script that handles the speech in the audio"""
from algorithms.speech.recognition import get_large_audio_transcription
from algorithms.speech.script_match import matching


def process_speech(audio_path: str, script_path: str) -> list:
    transcript, intervals = get_large_audio_transcription(audio_path)
    list_of_jokes = matching(transcript, intervals, script_path)
    return list_of_jokes
