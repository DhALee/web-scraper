import os
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Ollama LLM을 초기화합니다.
llama_model = Ollama(model="llama3.1:70b")

# 프롬프트 템플릿을 정의합니다.
prompt_template = PromptTemplate(
    input_variables=["file_content"],
    template="""
    I want you to act as a cashback offer summarizer for card companies. I will provide details about a specific cashback promotion from a card issuer, 
    and you will condense the information into a summary that can be viewed immediately. The summary should be structured into the following seven categories:
    
    1) **카드사명** (Card issuer):  
    - Name of the card company offering the promotion.
    2) **최대 혜택 금액** (Maximum benefit amount):  
    - The maximum amount that a customer can win in this promotion. If there are multiple events within the promotion, the maximum offer amount should be the sum of all events. For example:  
    *Event 1: 90,000 won, Event 2: 10,000 won, Event 3: 30,000 won* — Maximum offer: **130,000 won**.
    
    3) **이벤트 대상 카드** (Eligible cards for the event):  
    - List the eligible cards for the promotion.
    
    4) **이벤트 혜택 대상** (Customers eligible for the offer):  
    - Specify which customers are eligible for the promotion. If there are multiple events, describe the eligibility for each. (e.g., *Event 1: Customers with no activity in the past 6 months, Event 2: New customers*)
    
    5) **이벤트 대상 카드의 연회비** (Annual fee of the eligible cards):  
    - List the annual fees for each eligible card. For example:  
        - 처음: 해외겸용(MASTER) 18,000원, 국내전용(Local) 15,000원  
        - Mr.Life: 해외겸용(VISA) 18,000원, 국내(S&) 15,000원  
    
    6) **이벤트의 상세내용** (Details of the event offer):  
    - Describe how much customers need to spend to qualify for the cashback. (e.g., *Spend over 200,000 won to receive 100,000 won cashback, spend at international merchants for 60,000 won cashback*)
    
    7) **이벤트 기간** (Target time period):  
    - The validity period of the promotion. (e.g., *January 1, 2024 ~ March 31, 2024*)
    
    Please display the output in a clear format immediately after summarizing the promotion so it can be easily read without needing an Excel file    

    The following is the content of the cashback promotion:
    {file_content}
    """
)

# 텍스트 파일의 내용을 읽어오는 함수
def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# LLMChain을 생성합니다.
llama_chain = prompt_template | llama_model

# 텍스트 파일을 입력받고 사용자가 추가 입력을 할 수 있는 함수
def get_llama_response_from_file(file_path):
    # 파일 내용을 읽어옵니다.
    file_content = read_text_file(file_path)
    
    # 파일 내용과 사용자의 질문을 이용하여 프롬프트 생성 및 실행
    response = llama_chain.invoke({"file_content": file_content})
    return response

if __name__ == "__main__":
    for file in os.listdir('/svc/project/genaipilot/web-scraper/cg_files'):
        file_path = f'/svc/project/genaipilot/web-scraper/cg_files/{file}'
        response = get_llama_response_from_file(file_path)
        print("응답:", response)
        
        with open(f'/svc/project/genaipilot/web-scraper/summary/{file}', 'w', encoding='utf-8') as f:
            f.write(response)