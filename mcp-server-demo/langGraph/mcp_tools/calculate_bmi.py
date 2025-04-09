import asyncio
from langchain_core.tools import Tool
from ..tool_runner import mcp_tool_function
from ..parser import parse_bmi_params

def build():
    def run(query: str) -> str:
        params = parse_bmi_params(query)
        return asyncio.run(mcp_tool_function(
            command="python",
            args=["/Users/sin/PycharmProjects/DIProject/mcp-server-demo/server.py"],
            tool_name="calculate_bmi",
            tool_args=params
        ))

    return Tool.from_function(
        name="calculate_bmi",
        description="计算BMI的工具",
        func=run
    )