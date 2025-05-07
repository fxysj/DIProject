#多轮对话 用户打断的示例
# 旅行建议示例¶
# 在这个示例中，我们将构建一个旅行助手代理团队，它们可以通过交接相互沟通。
#
# 我们将创建3个代理：
#
# travel_advisor（旅行顾问）：可以帮助提供一般旅行目的地推荐。可以向sightseeing_advisor（观光顾问）和hotel_advisor（酒店顾问）寻求帮助。
# sightseeing_advisor（观光顾问）：可以帮助提供观光推荐。可以向travel_advisor和hotel_advisor寻求帮助。
# hotel_advisor（酒店顾问）：可以帮助提供酒店推荐。可以向sightseeing_advisor和travel_advisor寻求帮助。
# 这是一个完全连接的网络 - 每个代理都可以与任何其他代理交谈。
#
# 为了在代理之间实现交接，我们将使用具有结构化输出的LLMs。每个代理的LLM将返回一个输出，其中包含其文本响应（response）以及下一个路由代理（goto）。如果代理有足够的信息来回应用户，goto将设置为human，以便回到人类那里收集信息。
#现在我们 让我们定义我们的代理节点和图形
import os
from enum import Enum

from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from typing_extensions import TypedDict,Type

from langchain_core.messages import AnyMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph import MessagesState, StateGraph
from langgraph.types import Command, interrupt
from pydantic import BaseModel, Field
from typing_extensions import Literal

load_dotenv(verbose=True)

model = ChatOpenAI(model="gpt-4o",base_url=os.getenv("OPENAI_API_BASE_URL"),api_key=os.getenv("OPENAI_API_KEY"))

#为每个代理节点定义一个 帮助器以提供调用
def call_llm(messages:list[AnyMessage],target_agent_nodes:list[str]):
    """
    Call LLM with structured output to get a natural language response as well as a target agent (node) to go to next.

        Args:
            messages: list of messages to pass to the LLM
            target_agents: list of the node names of the target agents to navigate to
        """
    # 定义结构化输出的JSON架构：
    # - model's text response (`response`)
    # - name of the node to go to next (or 'finish')
    # see more on structured output here https://python.langchain.com/docs/concepts/structured_outputs

    # 动态构建 Literal 类型
    GotoLiteral = Literal[tuple(target_agent_nodes + ["finish"])]

    class Response(BaseModel):
        response: str=Field(description="A human readable response to the original question. Does not need to be a final response. Will be streamed back to the user.")
        goto: GotoLiteral= Field(
            ...,
            description="The next agent to call, or 'finish' if the user's query has been resolved. Must be one of the specified values."
        )

    response = model.with_structured_output(Response).invoke(messages)

    return response

def travel_advisor(state:MessagesState)->Command[Literal["sightseeing_advisor", "hotel_advisor", "human"]]:
    system_prompt = (
        "You are a general travel expert that can recommend travel destinations (e.g. countries, cities, etc). "
        "If you need specific sightseeing recommendations, ask 'sightseeing_advisor' for help. "
        "If you need hotel recommendations, ask 'hotel_advisor' for help. "
        "If you have enough information to respond to the user, return 'finish'. "
        "Never mention other agents by name."
    )
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    target_agent_nodes = ["sightseeing_advisor", "hotel_advisor"]
    response= call_llm(messages, target_agent_nodes)
    print(response)
    ai_msg = {"role": "ai", "content": response.response, "name": "travel_advisor"}
    # handoff to another agent or go to the human when agent is done
    goto = response.goto
    if goto == "finish":
        goto = "human"

    return Command(goto=goto, update={"messages": [ai_msg]})


def sightseeing_advisor(
    state: MessagesState,
) -> Command[Literal["travel_advisor", "hotel_advisor", "human"]]:
    system_prompt = (
        "You are a travel expert that can provide specific sightseeing recommendations for a given destination. "
        "If you need general travel help, go to 'travel_advisor' for help. "
        "If you need hotel recommendations, go to 'hotel_advisor' for help. "
        "If you have enough information to respond to the user, return 'finish'. "
        "Never mention other agents by name."
    )
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    target_agent_nodes = ["travel_advisor", "hotel_advisor"]
    response = call_llm(messages, target_agent_nodes)
    ai_msg = {
        "role": "ai",
        "content": response.response,
        "name": "sightseeing_advisor",
    }
    # handoff to another agent or go to the human when agent is done
    goto = response.goto
    if goto == "finish":
        goto = "human"

    return Command(goto=goto, update={"messages": [ai_msg]})

def hotel_advisor(
    state: MessagesState,
) -> Command[Literal["travel_advisor", "sightseeing_advisor", "human"]]:
    system_prompt = (
        "You are a travel expert that can provide hotel recommendations for a given destination. "
        "If you need general travel help, ask 'travel_advisor' for help. "
        "If you need specific sightseeing recommendations, ask 'sightseeing_advisor' for help. "
        "If you have enough information to respond to the user, return 'finish'. "
        "Never mention other agents by name."
    )
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    target_agent_nodes = ["travel_advisor", "sightseeing_advisor"]
    response = call_llm(messages, target_agent_nodes)
    ai_msg = {"role": "ai", "content": response.response, "name": "hotel_advisor"}
    # handoff to another agent or go to the human when agent is done
    goto = response.goto
    if goto == "finish":
        goto = "human"

    return Command(goto=goto, update={"messages": [ai_msg]})


def human_node(
    state: MessagesState,
) -> Command[
    Literal["hotel_advisor", "sightseeing_advisor", "travel_advisor", "human"]
]:
    """用于收集用户输入的节点。"""
    user_input = interrupt(value="Ready for user input.")

    active_agent = None

    # This will look up the active agent.
    for message in state["messages"][::-1]:
        if message.name:
            active_agent = message.name
            break
    else:
        raise AssertionError("Could not determine the active agent.")

    return Command(
        update={
            "messages": [
                {
                    "role": "human",
                    "content": user_input,
                }
            ]
        },
        goto=active_agent,
    )

builder = StateGraph(MessagesState)
builder.add_node("travel_advisor", travel_advisor)
builder.add_node("sightseeing_advisor", sightseeing_advisor)
builder.add_node("hotel_advisor", hotel_advisor)
# This adds a node to collect human input, which will route
# back to the active agent.
builder.add_node("human", human_node)
# We'll always start with a general travel advisor.
builder.add_edge(START, "travel_advisor")
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
from IPython.display import display, Image

display(Image(graph.get_graph().draw_mermaid_png()))

