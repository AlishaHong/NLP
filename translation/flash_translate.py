import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import json


def generate():
    vertexai.init(project="sesac-24-123", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
    )
    responses = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    print(responses)

text1 = """You are an expert Translator. 
You are tasked to translate documents from en to fr.
Please provide an accurate translation of this document and return translation text only: 
루브르 박물관에 가는 길을 알려주세요"""

generation_config = {
    "candidate_count": 1,
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 1,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]

generate()