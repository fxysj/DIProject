#文件IP封禁图
from langgraph.constants import START
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode
from ipForbitdeAgent.app.node.chat_node import ChatNode
from ipForbitdeAgent.app.node.chat_node import tools
from ipForbitdeAgent.app.node.tools_router import ToolsRouterNode
from ipForbitdeAgent.app.projo.MessageStateGloabel import MessageGraphGloabelState

#注入全局的信息
graph_builder = StateGraph(MessageGraphGloabelState)
#添加节点
toolNode= ToolNode(tools=tools)
graph_builder.add_node("chat",ChatNode.chat)
graph_builder.add_node("tools",toolNode)
graph_builder.add_edge("tools","chat")
graph_builder.add_conditional_edges(
    "chat",
     ToolsRouterNode.tools_router,
    {
        "tools":"tools",
        END:END
    }
)
graph_builder.add_edge(START, "chat")
graph = graph_builder.compile()
response = graph.invoke({"messages": [("user", "帮我查询一下上海天气")]})
print(response)