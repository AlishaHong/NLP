from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

# .env 파일에서 환경 변수 로드
load_dotenv()
# print(os.getcwd())
# 환경 변수에서 API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
# print(api_key)
# OpenAI 클라이언트 생성 시 API 키 설정
# client = OpenAI(api_key=api_key)
client = OpenAI()

# 음성 파일 저장 경로
speech_file_path = Path(__file__).parent / "speech1.mp3"

# 텍스트-음성 변환 요청
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!"
    # input = "hi"
)

# 음성 파일로 저장
response.stream_to_file(speech_file_path)

