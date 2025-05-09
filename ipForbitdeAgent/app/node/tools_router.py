from langgraph.constants import END
from typing_extensions import TypedDict

from ipForbitdeAgent.app.projo.MessageStateGloabel import MessageGraphGloabelState


class  ToolsRouterNode():

    @staticmethod
    def tools_router(state:MessageGraphGloabelState):
        """
           Use in the conditional_edge to route to the ToolNode if the last message
           has tool calls. Otherwise, route to the end.
           """
        messages = state.get("messages")
        if not messages:
            return END

        last_message = messages[-1]

        # 如果是 AI 发出且包含工具调用
        if last_message[0] == "ai" and hasattr(last_message[1], "tool_calls") and last_message[1].tool_calls:
            return "tools"

        # 工具调用完成后再进一次 chat，这时不再走 tools，应该结束
        return END