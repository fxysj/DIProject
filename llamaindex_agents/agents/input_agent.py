# 监听 UserInputEvent
import os
from dotenv import load_dotenv
import openai
from llamaindex_agents.agents.events import IntentEvent, SentimentEvent

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

def handle(event: IntentEvent) -> SentimentEvent | IntentEvent:
    text = event.text
    prompt = (
        f"请判断用户的意图（问答、闲聊、总结、投诉、未知）:\n{text}"
    )
    result = openai_completion(prompt).lower()

    valid_intents = ["问答", "闲聊", "总结", "投诉"]
    if any(intent in result for intent in valid_intents):
        # 取第一个匹配的意图
        matched = next((intent for intent in valid_intents if intent in result), "未知")
        event.intent = matched
        return SentimentEvent(text=text, intent=matched)
    else:
        event.intent = "未知"
        return event  # 重试

