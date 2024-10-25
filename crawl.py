import time
import os, sys

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

from crawl4ai.web_crawler import WebCrawler
from crawl4ai.crawler_strategy import *

# def delay(driver):
#     print("Delaying for 5 seconds...")
#     time.sleep(5)
#     print("Resuming...")

# def create_crawler():
#     crawler_strategy = LocalSeleniumCrawlerStrategy(verbose=True)
#     crawler_strategy.set_hook('after_get_url', delay)
#     crawler = WebCrawler(verbose=True, crawler_strategy=crawler_strategy)
#     crawler.warmup()
#     return crawler

def create_crawler():
    crawler = WebCrawler(verbose=True)
    crawler.warmup()
    return crawler

def title_content(text):

    llm = Ollama(model="llama3:70b")

    string_prompt = (
        PromptTemplate.from_template(("""I want you to take in the markdown of the entire webpage content and extract just the title and body of a news article {text}. 
                I will provide you with the {text} in markdown format, and you will separate the title and body of the article from that text and organize it neatly.

                All answers must be in Korean.
                                    """))
    )

    string_prompt_value = string_prompt.format_prompt(text=text)

    # print("-"*100)
    # print(string_prompt_value)

    result = llm.invoke(string_prompt_value)

    print(result)
    return result

def reputation_crawler(text):

    llm = Ollama(model="llama3:70b")

    string_prompt = (
        PromptTemplate.from_template(("""I want you to act as a reputation management system to collect and manage LOTTE Card's reputation through the news or the internet {text}. 
                                        I will provide you with a specific news article or online review {text}, and you will analyze the content, 
                                        classify whether LOTTE Card's reputation is positive, negative, or neutral, and summarize the main points. 
                                        In the case of a negative reputation, you will also include suggestions for improvement.
                                        If the text provided is not relevant to LOTTE Card, please write Null.

                                        All answers must be in Korean.
                                    """))
    )

    string_prompt_value = string_prompt.format_prompt(text=text)
    result = llm.invoke(string_prompt_value)

    print(result)

if __name__ == "__main__":
    url = sys.argv[1]

    crawler = create_crawler()
    result = crawler.run(url=url, bypass_cache=True)
    news = title_content(result.markdown)
    reputation_crawler(news)
