import asyncio

from dotenv import load_dotenv
from llama_index.core.workflow import JsonPickleSerializer, JsonSerializer
load_dotenv()

from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent
import os
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
from llama_index.core.workflow import Context
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b


def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b


llm = OpenAI(model="gpt-4o-mini", api_base=os.getenv("OPENAI_API_BASE_URL"),
             api_key=os.getenv("OPENAI_API_KEY"))


finance_tools = YahooFinanceToolSpec().to_tool_list()


finance_tools.extend([multiply, add])
workflow = FunctionAgent(
    name="Agent",
    description="Useful for performing financial operations.",
    tools=finance_tools,
    llm=llm,
    system_prompt="You are a helpful assistant.",
)
ctx = Context(workflow)
ctx_dict = ctx.to_dict(serializer=JsonSerializer())

restored_ctx = Context.from_dict(workflow,ctx_dict,serializer=JsonPickleSerializer())

async def set_name(ctx: Context, name: str) -> str:
    state = await ctx.get("state")
    state["name"] = name
    await ctx.set("state", state)
    return f"Name set to {name}"

async def fun():
    response = await workflow.run( user_msg="Hi, my name is Laurie!",ctx=ctx)
    print(response)
    response2 = await workflow.run(user_msg="What's my name?", ctx=restored_ctx)
    print(response2)

if __name__ == '__main__':
    asyncio.run(fun())
