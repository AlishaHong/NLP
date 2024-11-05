import google.generativeai as genai
import IPython.display
from dotenv import load_dotenv
import os
import time

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

file_path = 'C:/Users/SBA/NLP/videos/ndivia.mp4'
output_file_path = 'C:/Users/SBA/NLP/video_llm/output.txt'  # 출력 내용을 저장할 파일 경로

# 1. Upload and wait for processing:
uploaded_file = genai.upload_file(path=file_path)
print(f"Uploaded file URI: {uploaded_file.uri}")

while uploaded_file.state.name == "PROCESSING":
    print("processing video...")
    time.sleep(5)  # Wait for 5 seconds before checking again
    uploaded_file = genai.get_file(name=uploaded_file.name)  # Refresh file status

print("File processing complete!")

# 2. Gemini Video Q&A:
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
prompt = """
유튜브를 보고 아래에 답하세요.
- 대화내용을 모두 적어줘
"""
contents = [prompt, uploaded_file]
responses = model.generate_content(contents, stream=True, request_options={"timeout": 60*2})

# 비디오 출력
IPython.display.display(IPython.display.Video(file_path, width=800, embed=True))

# 응답을 파일로 저장
with open(output_file_path, 'w', encoding='utf-8') as file:
    for response in responses:
        file.write(response.text.strip())
        file.write("\n")  # 줄바꿈 추가
