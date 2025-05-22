# 监听 SentimentEvent
import os
from dotenv import load_dotenv
import openai
from llamaindex_agents.agents.events import SentimentEvent, QueryEvent

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_BASE_URL

def openai_completion(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

def handle(event: SentimentEvent) -> QueryEvent:
    text = event.text
    intent = event.intent
    prompt = f"请分析以下文本的情感倾向（正面、负面、中性）:\n{text}"
    sentiment = openai_completion(prompt).lower()

    # 简单取前三字防止意图识别失败
    if "正面" in sentiment:
        sentiment = "正面"
    elif "负面" in sentiment:
        sentiment = "负面"
    else:
        sentiment = "中性"

    event.sentiment = sentiment
    return QueryEvent(text=text, intent=intent, sentiment=sentiment)

