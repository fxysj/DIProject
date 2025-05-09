from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from ipForbitdeAgent.config import settings


class LLMFactory:
    @staticmethod
    def init_chat_mode(model="openai",provider="gpt-4o",api_key="",base_url="",tools=None):
       base_model =  init_chat_model(model=model,model_provider=provider,api_key=api_key,base_url=base_url)
       chat_model = base_model
       if tools:
           chat_model = base_model.bind_tools(tools=tools)

       return chat_model

    @staticmethod
    def getInitDefaultChatMode(tools=None):
        llm = LLMFactory.init_chat_mode(settings.Model, settings.Provider, settings.OPENAI_API_KEY,
                                        settings.OPENAI_API_BASE_URL,tools=tools)
        return llm


if __name__ == '__main__':
    llm = LLMFactory.init_chat_mode(settings.Model,settings.Provider,settings.OPENAI_API_KEY,settings.OPENAI_API_BASE_URL)
    response=llm.invoke([HumanMessage(content="你好")])
    print(response)
