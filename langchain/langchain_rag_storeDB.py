# build_vector_db.py
# 벡터디비에 저장

import google.generativeai as genai
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_upstage import UpstageEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("upstage_api_key")

loader = CSVLoader(
    file_path="한국산업은행_금융 관련 용어_20151231.csv", encoding="cp949"
)
pages = loader.load()
print(pages[:2])

us_model =  UpstageEmbeddings(
    api_key=api_key,
    model="solar-embedding-1-large"
)

Chroma.from_documents(pages, us_model, persist_directory="./database")

