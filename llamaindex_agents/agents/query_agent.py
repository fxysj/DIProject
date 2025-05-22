# 监听 QueryEvent
from llamaindex_agents.agents.events import QueryEvent, ResponseEvent

def handle(event: QueryEvent) -> ResponseEvent:
    # 这里调用你的知识库或模型
    summary = f"这是基于 '{event.text}' 的回答示例。"
    event.summary = summary
    return ResponseEvent(intent=event.intent, sentiment=event.sentiment, summary=summary)
