from langchain_core.runnables import RunnableLambda

async def reverse(s: str) -> str:
    return s[::-1]

chain = RunnableLambda(func=reverse)
events = [
    event async for event in chain.astream_events("hello",version="v2")
]
print(events)