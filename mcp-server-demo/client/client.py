from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


# Optional: create a sampling callback
async def handle_sampling_message(
        message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


# Tool function to initialize session and call resources/tools with flexible configuration
async def mcp_tool_function(
        command: str,
        args: list[str],
        tool_name: str,
        tool_args: dict
) -> str:
    # Create server parameters with provided values
    server_params = StdioServerParameters(
        command=command,
        args=args,
        env=None,  # Optional environment variables can be added
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
                read, write, sampling_callback=handle_sampling_message
        ) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            prompts = await session.list_prompts()

            # List available resources
            resources = await session.list_resources()

            # List available tools
            tools = await session.list_tools()

            # Call the specific tool with the provided arguments
            res = await session.call_tool(name=tool_name, arguments=tool_args)
            if not res.isError:
                result = res.content[0].text
                print(result)
                return result

            return "Tool call failed or resulted in an error"


# A wrapper to run the tool function asynchronously
async def run_tool_function():
    command = "python"
    args = ["/Users/sin/PycharmProjects/DIProject/mcp-server-demo/order_server.py"]
    #可以进行订单服务
    #用户服务都可以这样进行暴露到对应的函数即可
    tool_name = "calculate_bmi"
    tool_args = {"weight_kg": 1.2, "height_m": 2.1}

    result = await mcp_tool_function(command, args, tool_name, tool_args)
    print(f"Result from tool function: {result}")


# Main entry point
if __name__ == "__main__":
    import asyncio

    asyncio.run(run_tool_function())
