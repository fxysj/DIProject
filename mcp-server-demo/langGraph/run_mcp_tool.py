from tool_registry import registry

def run_mcp_tool(state: AgentState) -> AgentState:
    intent = state["intent"]
    if intent in registry:
        tool = registry[intent]()
        result = tool.run(state["query"])
        return {**state, "result": result}
    else:
        return {**state, "result": f"未知意图：{intent}"}
