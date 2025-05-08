import asyncio
from typing import AsyncGenerator, Dict, Any
from utils.memory import RedisMemory
from agents.langgraph_agent import LangGraphAgent
from agents.sentiment import analyze_sentiment
from agents.semantic import analyze_semantic

memory = RedisMemory()
agent = LangGraphAgent(memory=memory)

async def process_user_message(request, stream=True):
    user_message = request.messages[-1].content
    session_id = request.session_id
    # 记忆检索
    history = memory.get_history(session_id)
    # 情感分析
    sentiment = analyze_sentiment(user_message)
    # 语义分析
    semantic = analyze_semantic(user_message)
    # 智能体主流程
    if stream:
        async for chunk in agent.run_stream(user_message, history, sentiment, semantic, session_id):
            yield chunk
    else:
        result = await agent.run(user_message, history, sentiment, semantic, session_id)
        return result 