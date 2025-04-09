import asyncio
import os
from typing import TypedDict, Optional

from langchain_core.tools import Tool
from mcp import StdioServerParameters, stdio_client, ClientSession
from dotenv import load_dotenv
from openai import base_url

load_dotenv()


class AgentState(TypedDict):
    query: str
    intent: Optional[str]
    result: Optional[str]

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

llm = ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENAI_BASE_URL"))

intent_prompt = ChatPromptTemplate.from_template(
    """你是一个智能意图识别助手。请根据用户的提问内容，从以下意图中选择一个最匹配的：
- calculate_bmi：计算BMI
- translate_text：翻译文本
- generate_image：生成图片
- unknown：无法识别

用户说：{query}
请只返回意图关键词（如 calculate_bmi），不要添加其他文字。"""
)
async def mcp_tool_function(command: str, args: list, tool_name: str, tool_args: dict) -> str:
    server_params = StdioServerParameters(command=command, args=args)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            res = await session.call_tool(name=tool_name, arguments=tool_args)
            if not res.isError:
                return res.content[0].text
            return "MCP Tool call failed."

def build_mcp_tool(tool_name: str, tool_args: dict):
    async def _mcp_runner(query: str) -> str:
        return await mcp_tool_function(
            command="python",
            args=["/Users/sin/PycharmProjects/DIProject/mcp-server-demo/server.py"],
            tool_name=tool_name,
            tool_args=tool_args
        )

    def sync_runner(query: str) -> str:
        return asyncio.run(_mcp_runner(query))

    return Tool.from_function(
        name=tool_name,
        description="MCP Tool wrapper",
        func=sync_runner
    )

available_tools = {
    "calculate_bmi": "计算BMI",
    "translate_text": "翻译文本",
    "generate_image": "生成图片",
}
tool_list_text = "\n".join([f"- {k}：{v}" for k, v in available_tools.items()])
prompt_text = f"""你是一个智能意图识别助手。请根据用户的提问内容，从以下意图中选择一个最匹配的：
{tool_list_text}
用户说：{{query}}
请只返回意图关键词（如 calculate_bmi），不要添加其他文字。"""
intent_prompt = ChatPromptTemplate.from_template(prompt_text)
intent_runnable = (
    intent_prompt
    | llm
    | (lambda x: {"intent": x.content.strip()})  # 返回 dict
)
def update_intent_state(state: AgentState, update: dict) -> AgentState:
    return {**state, **update}


from langgraph.graph import StateGraph, END


def run_mcp_tool(state: AgentState) -> AgentState:
    intent = state["intent"]
    print(intent)
    if intent == "calculate_bmi":
        tool = build_mcp_tool("calculate_bmi", {"weight_kg": 70, "height_m": 1.75})
    else:
        return {**state, "result": f"未知意图：{intent}"}

    result = tool.run(state["query"])
    return {**state, "result": result}


# 路由逻辑（如果你有多个分支）
def router(state: AgentState) -> str:
    intent = state.get("intent", "")
    if intent == "计算BMI":
        return "call_mcp"
    return "fallback"


# fallback 节点
def fallback_handler(state: AgentState) -> AgentState:
    return {**state, "result": "❌ 无法识别意图或工具未实现。"}


# 构建图
graph = StateGraph(AgentState)
graph.add_node("detect_intent", intent_runnable | RunnableLambda(lambda update: update))
graph.add_node("call_mcp", RunnableLambda(run_mcp_tool))
graph.add_node("fallback", RunnableLambda(fallback_handler))

graph.set_entry_point("detect_intent")
graph.add_conditional_edges("detect_intent", router)
graph.set_finish_point("call_mcp")
graph.set_finish_point("fallback")

workflow = graph.compile()

state = {"query": "请帮我计算一下 BMI，体重70公斤，身高1米75"}
result = workflow.invoke(state)
print(result)
print("✅ 最终结果:", result["result"])
