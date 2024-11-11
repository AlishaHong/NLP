# retrieve.py
from langchain_upstage import UpstageEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv


# 환경변수 가져오기 
load_dotenv()
api_key = os.getenv("upstage_api_key")

# upstage의 임베딩 모델 선택 : 한국어에 최적화되었다고 함 
us_model = UpstageEmbeddings(
    api_key=api_key, model="solar-embedding-1-large"
)

# db생성 및 저장 : Chroma
vector_store = Chroma(persist_directory="./database", embedding_function=us_model)

# 검색기 
retriever = vector_store.as_retriever(
    search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10}
)
# search_type="mmr" : maximal marginal relevance 알고리즘(검색결과의 다양성을 높임)
# K : 최종적으로 반환할 문서 수 
# fetch_k : 처음에 가져올 후보 문서 수(그 중 k개를 최종선택함)


# 템플릿
template = """
[context]: {context}
---
[질의]: {query}
---
[예시]
신용 환산율입니다.
---
위의 [context] 정보 내에서 [질의]에 대해 답변 [예시]와 같이 술어를 붙여서 답하세요.
"""

prompt = ChatPromptTemplate.from_template(template)
# ChatPromptTemplate : 프롬프트 템플릿을 설정하고 관리하는 클래스
# 특정 형식의 프롬프트를 템플릿화하여 변수를 동적으로 삽입하고
# 언어모델에 전달할 준비된 프롬프트를 생성하기 위함
# prompt = hub.pull("rlm/rag-prompt") hub.pull()은 외부에서 리소스를 가져오는 개념 

# 랭체인을 
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
# ChatGoogleGenerativeAI : Google의 대화형 언어 모델을 호출할 수 있는 클래스


def merge_pages(pages):
    merged = "\n\n".join(page.page_content for page in pages)
    print(f"참조 문서 시작==>[\n{merged}\n]<==참조 문서 끝")
    return merged

# 체인 
chain = (
    {"query": RunnablePassthrough(), "context": retriever | merge_pages}
    | prompt
    | llm
    | StrOutputParser() #언어모델이 생성한 응답을 문자열 형식으로 파싱 
)
# RunnablePassthrough() : 입력을 변환하지 않고 그대로 전달하는 역할
# 파이프라인을 구성할 때 중간에 값을 변경하지 않고자 함 
# retriever를 통해 추출한 내용을 병합함(merge_pages )


# 실행 
answer = chain.invoke(
    "짧은 기간 동안의 차익을 위해 금융사가 보유하는 걸 뜻하는 용어가 뭐야?"
)
print(f"answer1: {answer}\n\n")

answer = chain.invoke("트레이딩 포지션이 뭐야?")
print(f"answer2: {answer}")
