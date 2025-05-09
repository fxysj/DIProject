#全局进行主图和子图共享的状态信息
from langchain_core.documents import Document
from typing_extensions import Any

from ipForbitdeAgent.app.vo.MessageInputRequest import MessageInputRequest

#注入请求的对象信息
class MessageGraphGloabelState(MessageInputRequest):
    chat_history:list[str]=None #历史对话信息 类似为 user:xxx,ai:xxx,tools:xxx,ansitis:xxx
    reterive_documents:list[Document]=None #检索到的文档信息是一个列表
    next:str#下一个调度的节点信息
    result:Any=None
