# 监听 ResponseEvent
from llamaindex_agents.agents.events import ResponseEvent

def handle(event: ResponseEvent) -> ResponseEvent:
    message = (
        f"[最终回复]\n"
        f"意图: {event.intent}\n"
        f"情绪: {event.sentiment}\n"
        f"回答: {event.summary}"
    )
    event.message = message
    return event
