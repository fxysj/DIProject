import asyncio
import os

from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
async def main():
    # 初始化 MCP 客户端，连接多个 MCP 服务器
    client = MultiServerMCPClient(
        {
            "weather": {
                # 确保你的天气服务器在端口 8000 上运行
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    # 获取工具列表
    tools = await client.get_tools()
    print(tools)
    from dotenv import load_dotenv
    load_dotenv(verbose=True)
    #     callbacks.append(ThoughtCaptureHandler(initial_state))
    llm = ChatOpenAI(
        model="claude-3-7-sonnet-latest",
        temperature=0.3,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("BASE_URL"),
        # streaming=True,  # 关键：streaming 为 True 才会逐 token 触发 on_llm_new_token
        # callbacks=callbacks
    )
    model = init_chat_model(
        "openai:gpt-4o",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("BASE_URL"),
    )

    # 创建 ReAct Agent，使用指定的模型和工具
    agent = create_react_agent(
        model=model,
        tools=tools,
    )

    # 使用 Agent 处理数学问题
    # math_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    # )
    # print("Math Response:", math_response)

    # 使用 Agent 处理天气查询
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
    )
    print("Weather Response:", weather_response)

# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())
