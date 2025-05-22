# 监听 IntentEvent
from llamaindex_agents.agents.events import IntentEvent, SentimentEvent

def handle(event: IntentEvent) -> SentimentEvent | IntentEvent:
    text = event.text
    # 简单意图判断示范
    if "问题" in text:
        intent = "问答"
    elif "你好" in text:
        intent = "闲聊"
    else:
        intent = "未知"

    event.intent = intent
    if intent == "未知":
        # 返回自己，代表重试意图识别
        return event
    return SentimentEvent(text=text, intent=intent)
