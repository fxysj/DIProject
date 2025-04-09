from langchain.tools import Tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio


async def mcp_tool_function(command: str, args: list, tool_name: str, tool_args: dict) -> str:
    server_params = StdioServerParameters(command=command, args=args)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            res = await session.call_tool(name=tool_name, arguments=tool_args)
            if not res.isError:
                return res.content[0].text
            return "MCP Tool call failed."


def build_mcp_tool(config: dict):
    async def _mcp_runner(query: str) -> str:
        return await mcp_tool_function(
            command=config["command"],
            args=config["args"],
            tool_name=config["tool_name"],
            tool_args=config["tool_args"]
        )

    def sync_runner(query: str) -> str:
        return asyncio.run(_mcp_runner(query))

    return Tool.from_function(
        name="mcp_tool",
        description="调用 MCP 后端工具",
        func=sync_runner
    )

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# 创建状态结构
from typing import TypedDict, Optional


class AgentState(TypedDict):
    query: str
    intent: Optional[str]
    result: Optional[str]

# MCP 工具配置
config = {
    "command": "python",
    "args": ["/Users/sin/PycharmProjects/DIProject/mcp-server-demo/server.py"],
    "tool_name": "calculate_bmi",
    "tool_args": {"weight_kg": 70, "height_m": 1.75}
}

# 构建 MCP 工具
mcp_tool = build_mcp_tool(config)

# 用 LangGraph 封装 MCP 工具节点
def run_mcp_node(state: AgentState) -> AgentState:
    print(state.get("query"))
    result = mcp_tool.run(state["query"])
    return {"query": state["query"], "result": result}

# 初始化 LangGraph 状态图
workflow = StateGraph(AgentState)
workflow.add_node("call_mcp", RunnableLambda(run_mcp_node))
workflow.set_entry_point("call_mcp")
workflow.set_finish_point("call_mcp")

graph = workflow.compile()

# 示例调用
input_state = {"query": "你好"}
final_state = graph.invoke(input_state)

print("✅ 最终结果:", final_state["result"])
