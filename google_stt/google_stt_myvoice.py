from google.cloud import speech
import pyaudio
import keyboard  # keyboard 라이브러리 임포트
import os

# Google Cloud Speech-to-Text 클라이언트 초기화
client = speech.SpeechClient()

# PyAudio 초기화
p = pyaudio.PyAudio()

# 마이크 입력 설정
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=48000,
                input=True,
                frames_per_buffer=1024)

# 음성 데이터를 담을 버퍼
audio_content = []

print("녹음 시작 (말하기 시작하세요). 'q' 키를 누르면 녹음이 종료됩니다.")

# 음성 녹음 루프
while True:
    # 마이크에서 데이터 읽기
    data = stream.read(1024)
    audio_content.append(data)

    # 'q' 키를 누르면 녹음 종료
    if keyboard.is_pressed('q'):  # keyboard 라이브러리 사용
        print("녹음 종료")
        break

# 스트림 닫기
stream.stop_stream()
stream.close()

# PyAudio 닫기
p.terminate()

# 음성 데이터를 합치기qq
audio_content = b''.join(audio_content)

# 음성 인식 설정
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=48000,
    language_code="ko-KR",  # 한국어로 설정
    model="default",
    audio_channel_count=1,
    enable_word_confidence=True,
    enable_word_time_offsets=True,
)

# 음성 데이터를 Speech-to-Text API로 전송
audio = speech.RecognitionAudio(content=audio_content)
operation = client.long_running_recognize(config=config, audio=audio)

print("음성 인식 진행 중...")

# 인식 결과를 기다림
response = operation.result(timeout=90)

# 파일 이름에 숫자를 붙이기
base_filename = "transcript"
file_number = 1
while os.path.exists(f"{base_filename}{file_number}.txt"):
    file_number += 1
filename = f"{base_filename}{file_number}.txt"

# 결과를 새 파일에 저장
with open(filename, "w", encoding="utf-8") as f:
    for result in response.results:
        transcript = result.alternatives[0].transcript
        f.write(f"Transcript: {transcript}\n")
        print(f"Transcript: {transcript}")

print("음성 인식 결과가 transcript.txt 파일에 저장되었습니다.")