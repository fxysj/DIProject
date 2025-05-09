#聊天的节点 正常返回的节点
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.utils import Output
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from ipForbitdeAgent.app.llm.init_chat_mode import LLMFactory
from ipForbitdeAgent.app.projo.MessageStateGloabel import MessageGraphGloabelState
from langchain.tools import tool

from ipForbitdeAgent.app.templates.ip_forbi_prompts import IPFORBIPRO
from ipForbitdeAgent.app.vo.MessageInputRequest import MessageInputRequest


@tool
def get_weather(user_input:str):
   """获取天气信息
   Args:
      user_input: 用户输入
   Returns:
       返回天气信息
   """
   return "晴天"

tools = [get_weather]


class ChatResponse(TypedDict):
   content:str=Field(...,description="系统友好回复")

class ChatNode:
   @staticmethod
   def chat(state:MessageGraphGloabelState):
      promt= PromptTemplate(
         template=IPFORBIPRO,
         input_variables=["messages"],
      )
      llm = LLMFactory.getInitDefaultChatMode(tools=tools)
      messages = state["messages"][-1].content
      response = llm.invoke(messages)
      return  {"messages":[response]}

if __name__ == '__main__':
    messages  = [("user", "上海天气")]
    m = MessageGraphGloabelState(messages=messages,reterive_documents=[],chat_history=[])
    response:MessageGraphGloabelState = ChatNode.chat(m)
    print(response)





