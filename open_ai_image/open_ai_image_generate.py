from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

# .env 파일에서 환경 변수 로드
load_dotenv()


# 환경 변수에서 API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
# OpenAI 클라이언트 생성 시 API 키 설정
# client = OpenAI(api_key=api_key)
client = OpenAI()

response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print("Generated Image URL:", image_url)