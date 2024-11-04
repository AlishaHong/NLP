# 실시간으로 음성출력 
# pip install pyaudio

from google.cloud import texttospeech
import pyaudio

client = texttospeech.TextToSpeechClient()
text="오늘 날씨가 화창하네!"
input_text = texttospeech.SynthesisInput(text=text)

voice = texttospeech.VoiceSelectionParams(
    language_code="ko-KR",  # 한국어로 변경
    name="ko-KR-Standard-D",  # 한국어 음성 이름 선택 
)

# 속도 조절 (0.5는 기본 속도의 절반)
speaking_rate = 1
sample_rate = 44100
sample_rate_hertz=24000,

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    speaking_rate=speaking_rate  # 속도 설정
)

response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config}
)

# PyAudio 초기화
p = pyaudio.PyAudio()

# 출력 스트림 생성
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True)

# 음성 데이터를 스트림으로 출력
stream.write(response.audio_content)

# 스트림 닫기
stream.stop_stream()
stream.close()

# PyAudio 닫기
p.terminate()

print('음성 출력 완료')