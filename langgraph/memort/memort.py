from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableAssign
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
load_dotenv(verbose=True)
p = PromptTemplate(
    template="""历史信息:
    {chat_history}
    用户输入:{user_input}
    根据用户输入和历史信息 回复用户
    """,
    input_variables=["chat_history","user_input"],
)

llm = ChatOpenAI(model="gpt-4o",base_url=os.getenv("OPENAI_API_BASE_URL"),api_key=os.getenv("OPENAI_API_KEY"))

m = ConversationBufferMemory(memory_key="chat_history",)

chain = LLMChain(
    llm=llm,
    prompt=p,
    memory=m,
    verbose=True,
)
c = RunnableAssign({"chat_history": m.dict()}) | p | llm
print(chain.invoke({"user_input":"那就好"}))
print(c.invoke({"user_input":"刚才我说了什么"}))


