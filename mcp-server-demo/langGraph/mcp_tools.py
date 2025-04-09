import asyncio
from typing import Callable

from langchain_core.tools import Tool
from mcp import stdio_client, ClientSession, StdioServerParameters

from config import MCP_SERVER_COMMAND, MCP_SERVER_ARGS


async def mcp_tool_function(command: str, args: list, tool_name: str, tool_args: dict) -> str:
    server_params = StdioServerParameters(command=command, args=args)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            res = await session.call_tool(name=tool_name, arguments=tool_args)
            if not res.isError:
                return res.content[0].text
            return "MCP Tool 调用失败 ❌"

def build_mcp_tool(tool_name: str, tool_args: dict) -> Tool:
    async def _mcp_runner(query: str) -> str:
        return await mcp_tool_function(MCP_SERVER_COMMAND, MCP_SERVER_ARGS, tool_name, tool_args)

    def sync_runner(query: str) -> str:
        return asyncio.run(_mcp_runner(query))

    return Tool.from_function(
        name=tool_name,
        description=f"本地 MCP 工具调用：{tool_name}",
        func=sync_runner,
    )
