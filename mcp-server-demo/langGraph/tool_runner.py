import asyncio
from mcp import StdioServerParameters, stdio_client, ClientSession

async def mcp_tool_function(command: str, args: list, tool_name: str, tool_args: dict) -> str:
    server_params = StdioServerParameters(command=command, args=args)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            res = await session.call_tool(name=tool_name, arguments=tool_args)
            if not res.isError:
                return res.content[0].text
            return "MCP Tool call failed."