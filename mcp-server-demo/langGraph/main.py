import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

from tool_registry import registry  # 你要自己提供 registry 工具注册模块

load_dotenv()


class AgentState(TypedDict):
    query: str
    intent: Optional[str]
    result: Optional[str]


# 定义可用工具及意图
available_tools = {
    "calculate_bmi": "计算BMI",
    "translate_text": "翻译文本",
    "generate_image": "生成图片",
}

tool_list_text = "\n".join([f"- {k}：{v}" for k, v in available_tools.items()])

# 意图识别 Prompt
intent_prompt = ChatPromptTemplate.from_template(f"""
你是一个智能意图识别助手。请根据用户的提问内容，从以下意图中选择一个最匹配的：
{tool_list_text}
用户说：{{query}}
请只返回意图关键词（如 calculate_bmi），不要添加其他文字。
""")

# OpenAI 模型
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_BASE_URL")
)

# 完整意图链条
intent_chain = intent_prompt | llm | StrOutputParser()

# Intent识别逻辑
def intent_parse(state: AgentState) -> AgentState:
    query = str(state["query"])
    print("📥 用户输入:", query)
    intent = intent_chain.invoke({"query": query}).strip()
    print("🔍 识别意图:", intent)
    return {**state, "intent": intent}

# MCP工具执行逻辑
def run_mcp_tool(state: AgentState) -> AgentState:
    intent = state.get("intent")
    query = state.get("query")
    if intent in registry:
        tool = registry[intent]()
        result = tool.run(query)
        return {**state, "result": result}
    return {**state, "result": f"未知意图：{intent}"}

# 分支路由
def router(state: AgentState) -> str:
    intent = state.get("intent", "")
    return "call_mcp" if intent in registry else "fallback"

# 兜底处理
def fallback_handler(state: AgentState) -> AgentState:
    return {**state, "result": "❌ 无法识别意图或工具未实现。"}

# 构建LangGraph
graph = StateGraph(AgentState)
graph.add_node("detect_intent", intent_parse)
graph.add_node("call_mcp", RunnableLambda(run_mcp_tool))
graph.add_node("fallback", RunnableLambda(fallback_handler))

graph.set_entry_point("detect_intent")
graph.add_conditional_edges("detect_intent", router)
graph.set_finish_point("call_mcp")
graph.set_finish_point("fallback")

workflow = graph.compile()


async def run():
    query_text = "请帮我计算一下 BMI，体重70公斤，身高1米75"
    print("🧪 开始测试：", query_text)
    state = {"query": query_text}
    result = await workflow.ainvoke(state)
    print("✅ 最终结果:", result)


# 运行测试
import asyncio

if __name__ == '__main__':
    asyncio.run(run())
