import asyncio

from llama_index.core import chat_engine
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.chat_engine.types import StreamingAgentChatResponse
from llama_index.tools.tavily_research import TavilyToolSpec
from llamaindex.factoryLLM import factoryLLM
from llama_index.core.agent.workflow import AgentStream
llm=factoryLLM()
import os
tavily_tool = TavilyToolSpec(api_key=os.getenv("TAVILY_API_KEY"))
workflow = FunctionAgent(
    tools=tavily_tool.to_tool_list(),
    llm=llm,
    system_prompt="You're a helpful assistant that can search the web for information.",
)


async def main():
    handler = workflow.run(user_msg="What's the weather like in San Francisco?")

    async for event in handler.stream_events():
        if isinstance(event, AgentStream):
            print(event.delta, end="", flush=True)

if __name__ == '__main__':
    asyncio.run(main())
