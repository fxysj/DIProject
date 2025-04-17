import asyncio

from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.workflow import Context
from dotenv import load_dotenv
from llama_index.core.workflow import JsonPickleSerializer, JsonSerializer
load_dotenv()
import os
from llamaindex.agent import workflow
from llama_index.llms.openai import OpenAI

async def set_name(ctx: Context, name: str,role:str) -> str:
    state = await ctx.get("state")
    state["name"] = name
    state["role"] = role
    await ctx.set("state", state)
    return f"Name set to {name} role set to {role}"


llm = OpenAI(model="gpt-4o-mini", api_base=os.getenv("OPENAI_API_BASE_URL"),
             api_key=os.getenv("OPENAI_API_KEY"))

workflow = AgentWorkflow.from_tools_or_functions(
    [set_name],
    llm=llm,
    system_prompt="You are a helpful assistant that can set a name.",
    initial_state={"name": "unset","role":"sys"},
)

ctx = Context(workflow)
async def func():
    response = await workflow.run(user_msg="What's my name? my role is ?", ctx=ctx)
    print(str(response))
    response2 = await workflow.run(user_msg="My name is Laurie my role is ai", ctx=ctx)
    print(str(response2))
    state = await ctx.get("state")
    print(state)
    print("Name as stored in state: ", state["name"])
# check if it knows a name before setting it
if __name__ == '__main__':
    asyncio.run(func())
