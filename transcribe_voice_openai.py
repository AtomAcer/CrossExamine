# package imports
import tempfile
import base64
import streamlit as st
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_KEY"]


def record_and_transcribe(client, audio_bytes):

    # save recording
    filename = "Question.wav"
    with open(filename, "wb") as f:
        f.write(audio_bytes)

    # Pass the audio file to the model for transcription
    with open(filename, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="text",
            language="en"
        )
    
    # Ensure the file is deleted
    if os.path.exists(filename):
        os.remove(filename)

    return transcript

# def record_and_transcribe(client, audio_bytes):
#     # Create a temporary file
#     with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp_audio_file:
#         # Write the audio bytes to the temporary file
#         temp_audio_file.write(audio_bytes)
#         temp_audio_file.flush()  # Ensure the data is written

#         # Pass the temporary file to the model for transcription
#         transcript = client.audio.transcriptions.create(
#             file=temp_audio_file,
#             model="whisper-1",
#             response_format="text",
#             language="en"
#         )

#     return transcript



def create_output_speech(client, response_text, voice="alloy"):
    """
    Create a speech output from text using TTS model and save as WAV file.

    Args:
        client: API client for audio processing
        response_text (str): Text to be converted to speech
        voice (str): Voice style for the speech, default is "alloy"

    Returns:
        None
    """
    with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice=voice,
            input=response_text,
    ) as response:
        response.stream_to_file("speech.wav")
    return

def convert_audio_to_base64(audio_file_path):
    """
    Convert an audio file to base64 encoding.

    Args:
        audio_file_path (str): Path to the audio file

    Returns:
        str: Base64 encoded string of the audio file
    """
    with open(audio_file_path, 'rb') as f:
        audio_encoded = base64.b64encode(f.read()).decode('utf-8')
    return audio_encoded