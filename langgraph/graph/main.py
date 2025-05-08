import json
import os
import uuid

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage, BaseMessage
from pydantic import BaseModel

load_dotenv(verbose=True)

llm = ChatOpenAI(model="gpt-4o",
                 base_url=os.getenv("OPENAI_API_BASE_URL"),
                 api_key=os.getenv("OPENAI_API_KEY"),
                 temperature=0,
                 max_retries=2,
                 max_tokens=4096
                 )
pro = PromptTemplate(template="""
角色： 你是一个恋爱大师
目标： 对用户进行传递恋爱技巧
""",input_variables=["user_input"])

@tool
def getHobby(user_input):
    """获取兴趣爱好信息 当需要揣测用户的兴趣爱好时调用"""
    return "爱好篮球"

@tool
def getXin(user_input):
    """获取星座信息是调用"""
    return "星座信息"
tools=[getHobby,getXin]

llm_bind_tools = llm.bind_tools(tools)

chain =  llm_bind_tools


class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        print(outputs)
        return {"messages": outputs}



from pydantic import Field
class UserInfo(AIMessage):
    username: str = Field(default="anonymous")
    user_id: str = Field(default="unknown")




def agent_node(state:MessagesState):
    #这里必须是大模型返回的消息信息
    #可以进行扩展对应的的熟悉
    res = chain.invoke(state.get("messages"))

    u = UserInfo(**(res.model_dump()))
    u.username = "22"
    u.user_id="222"
    return {"messages":[u]}

tool_node = BasicToolNode(tools=tools)


def route_tools(
    state: MessagesState,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


builder = StateGraph(MessagesState)
builder.add_node("tools", tool_node)
builder.add_node("agent",agent_node)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent",
                                route_tools,
                              {"tools": "tools", END: END},
                              )
builder.add_edge("tools","agent")
memory =  MemorySaver()

graph = builder.compile(checkpointer=memory)
thread_config = {"configurable": {"thread_id": 2}}


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]},config=thread_config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
            print("Data:",value["messages"][-1].username)

#可以通过继承从方式
#base_model dict **res进行注入到方式
#可以进行封装在一起



while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
