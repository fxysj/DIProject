from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState


#定义请求对象类型用来接受用户传递的信息
class MessageInputRequest(MessagesState):
    pass


if __name__ == '__main__':
    mesages = {"messages":[HumanMessage(content="sin")]}
    me = MessageInputRequest(mesages)
    print(me)