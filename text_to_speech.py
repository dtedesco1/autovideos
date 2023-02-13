import os
import io
from google.cloud import texttospeech

# Initialize the Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

# Define the dictionary of questions and responses
questions_and_responses = {
    "What is your favorite hobby?": "My favorite hobby is reading and studying the law.",
    "What is your biggest accomplishment?": "My biggest accomplishment is preserving the Union and ending slavery during the Civil War.",
    "What is your most prized possession?": "My most prized possession is the Emancipation Proclamation, which declared freedom for all slaves in Confederate-held territory.",
}

# Loop through the questions and responses
for question, response in questions_and_responses.items():
    # Define the voice configuration for the question
    question_voice_config = texttospeech.types.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE,
        name="en-US-Wavenet-D",
    )

    # Define the audio configuration for the question
    question_audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
    )

    # Define the voice configuration for the response
    response_voice_config = texttospeech.types.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE,
        name="en-US-Wavenet-C",
    )

    # Define the audio configuration for the response
    response_audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
    )

    # Use the Google Cloud Text-to-Speech API to generate the question audio
    question_synthesis_input = texttospeech.types.SynthesisInput(text=question)
    question_audio = client.synthesize_speech(
        input=question_synthesis_input,
        voice=question_voice_config,
        audio_config=question_audio_config,
    )

    # Use the Google Cloud Text-to-Speech API to generate the response audio
    response_synthesis_input = texttospeech.types.SynthesisInput(text=response)
    response_audio = client.synthesize_speech(
        input=response_synthesis_input,
        voice=response_voice_config,
        audio_config=response_audio_config,
    )

    # Write the question audio to a file
    with io.BytesIO(question_audio.audio_content) as f:
        with open(f"{question.replace(' ', '_')}.mp3", "wb") as g:
            g.write(f.read())

    # Write the response audio to a file
    with io.BytesIO(response_audio.audio_content) as f:
        with open(f"{response.replace(' ', '_')}.mp3", "wb") as g:
            g.write(f.read())

