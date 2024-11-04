import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel
from google.cloud import speech
import pyaudio
import keyboard  # keyboard 라이브러리 임포트
import re
from google.cloud import texttospeech
import pyaudio


# 속도 조절 (0.5는 기본 속도의 절반)
speaking_rate = 1
sample_rate = 24000

def project_init(): 
    PROJECT_ID = "sesac-24-123"  # @param {type:"string"}
    LOCATION = "us-central1"  # @param {type:"string"}

    # STEP 1. VertexAI 초기화
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # STEP 2. Gemini 모델 가져오기
    model = GenerativeModel("gemini-1.5-flash")

    return model


def mic_rec():
    # STEP 4. PyAudio 초기화
    p = pyaudio.PyAudio()


    # 마이크 입력 설정
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=24000,
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
    return audio_content



def STT(audio_content, model): 
# 음성 데이터가 1024단위로 쪼개져서 리스트로 저장된것을 하나로 합치기
    audio_content = b''.join(audio_content)

    # Google Cloud STT 클라이언트 초기화
    client = speech.SpeechClient()
    # 음성 인식 설정
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
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

    # 결과 출력
    # results = []
    result_markdown = ""
    for result in response.results:
        result_markdown = model.generate_content(result.alternatives[0].transcript).text

    return result_markdown




def markdown_to_text(markdown_text):
  # 1. 헤더 제거
  text = re.sub(r'\#+ ', '', markdown_text)
  # 2. 굵은 글씨 제거
  text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
  # 3. 기타 마크다운 태그 제거
  text = re.sub(r'<[^>]+>', '', text)
  # 4. 줄 바꿈 제거
  text = text.replace('\n', ' ')
  return text.strip()



def TTS(plain_text):
    client = texttospeech.TextToSpeechClient()
    text=plain_text
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",  # 한국어로 변경
        name="ko-KR-Standard-D",  # 한국어 음성 이름 선택 
    )

    # # 속도 조절 (0.5는 기본 속도의 절반)
    # speaking_rate = 1
    # sample_rate = 24000

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,  # mono-24KHZ,strero 44.1KHz  
        speaking_rate=speaking_rate  # 속도 설정
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    return response



def play_audio(response):
    # PyAudio 초기화
    p = pyaudio.PyAudio()

    # 출력 스트림 생성
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # 음성 데이터를 스트림으로 출력
    stream.write(response.audio_content)

    # 스트림 닫기
    stream.stop_stream()
    stream.close()

    # PyAudio 닫기
    p.terminate()

    print('음성 출력 완료') 
    




model = project_init()
audio_content = mic_rec()
result_markdown = STT(audio_content, model)
plain_text = markdown_to_text(result_markdown)
response = TTS(plain_text)
play_audio(response)