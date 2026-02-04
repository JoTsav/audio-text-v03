import os
from dotenv import load_dotenv
from groq import Groq

"""
@author: Joseph
"""
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
# groq client for API key
client = Groq(api_key=API_KEY)

def transcribe_audio(file_path):
    """
    Transcribes an audio file into text using the "whisper" transcription model. The function
    reads the provided audio file, sends its content for transcription, and returns the resulting
    text. The transcription model used is optimized for large-scale audio input and maintains
    high accuracy and detail in the verbose JSON response format.

    :param file_path: The path to the audio file to be transcribed. Must be a valid file path
        pointing to an audio file.
    :type file_path: str
    :return: The transcribed text from the provided audio file.
    :rtype: str
    """
    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(file_path), file.read()),
            model = "whisper-large-v3-turbo",
            temperature=0, # no changes
            response_format="verbose_json",
        )
        return transcription.text
if __name__ == "__main__":
    import sys
    # parsing filename as default argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        # TODO: default placeholder
        filename = "temp_uploads/temp_audio.wav"
    if os.path.exists(filename) and os.path.isfile(filename):
        # do transcription
        print(f"Transcribing audio file: {filename}\n")
        print(transcribe_audio(filename))

    else:
        print(f"File not found: {filename}")
        print("Usage: transcription.py <path_to_audio_file>?? ")

