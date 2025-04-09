from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

from intents import intent_runnable
from mcp_tools import build_mcp_tool


class AgentState(TypedDict):
    query: str
    intent: Optional[str]
    result: Optional[str]


def update_intent_state(state: AgentState, update: dict) -> AgentState:
    return {**state, **update}


def run_mcp_tool(state: AgentState) -> AgentState:
    intent = state["intent"]
    if intent == "calculate_bmi":
        tool = build_mcp_tool("calculate_bmi", {"weight_kg": 70, "height_m": 1.75})
    else:
        return {**state, "result": f"未知意图：{intent}"}

    result = tool.run(state["query"])
    return {**state, "result": result}


def router(state: AgentState) -> str:
    intent = state.get("intent", "")
    if intent == "calculate_bmi":
        return "call_mcp"
    return "fallback"


def fallback_handler(state: AgentState) -> AgentState:
    return {**state, "result": "❌ 无法识别意图或工具未实现。"}


def build_workflow():
    graph = StateGraph(AgentState)
    graph.add_node("detect_intent", intent_runnable | RunnableLambda(lambda update: update))
    graph.add_node("call_mcp", RunnableLambda(run_mcp_tool))
    graph.add_node("fallback", RunnableLambda(fallback_handler))

    graph.set_entry_point("detect_intent")
    graph.add_conditional_edges("detect_intent", router)
    graph.set_finish_point("call_mcp")
    graph.set_finish_point("fallback")

    return graph.compile()
