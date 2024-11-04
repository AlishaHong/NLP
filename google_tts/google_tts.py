# 녹음파일 만들기 
# pip install google-cloud-texttospeech

"""Synthesizes speech from the input string of text."""
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

input_text = texttospeech.SynthesisInput(text="옥상으로따라와")

# Note: the voice can also be specified by name.
# Names of voices can be retrieved with client.list_voices().
voice = texttospeech.VoiceSelectionParams(
    # language_code="en-US",
    # name="en-US-Studio-O",
    language_code="ko-KR",  # 한국어로 변경
    name="ko-KR-Standard-A",  # 한국어 음성 이름 선택
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    speaking_rate=1     # 말하는 속도 
)

response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config}
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')