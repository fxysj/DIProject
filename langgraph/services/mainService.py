import os

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Annotated, Sequence, Literal

from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_core.tools import create_retriever_tool
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv(verbose=True)

def downDocuments():
    # 检索器
    # 首先索引三遍博客文章
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]
    docs = [WebBaseLoader(url).load() for url in urls]
    docks_list = [item for sublist in docs for item in sublist]
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100,
        chunk_overlap=50,
    )
    docs_split = text_splitter.split_documents(docks_list)
    # 添加到向量数据库库保存到文件中
    vectorstore = Chroma.from_documents(
        persist_directory="/Users/sin/PycharmProjects/DIProject/langgraph/services/chrom_db",
        documents=docs_split,
        collection_name="rag-chroma",
        embedding=OpenAIEmbeddings(base_url=os.getenv("OPENAI_API_BASE_URL"), api_key=os.getenv("OPENAI_API_KEY")),
    )
    return  vectorstore

def  getAsretirure(pre:str):
    print("./chrom_db init....")
    #downDocuments() #先执行存储
    vectorstore = Chroma(persist_directory=pre,collection_name="rag-chroma")
    return  vectorstore.as_retriever()




retriever = getAsretirure("/Users/sin/PycharmProjects/DIProject/langgraph/services/chrom_db")



# 创建一个检索工具
retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_blog_posts",
    "Search and return information about Lilian Weng blog posts on LLM agents, prompt engineering, and adversarial attacks on LLMs."
)
tools = [retriever_tool]


class AgentState(TypedDict):
    # add_messages 函数定义了如何处理更新
    # 默认是替换 add_messages 表示 append
    messages: Annotated[Sequence[BaseMessage], add_messages]


# 我们可以像 这样布局䘝自主的RAG图
# 状态是一组消息
# 每个节点将更新附加到状态
# 条件边决定下一个访问的节点
# Agent(node)  shouldRetrive Condtional Endge  Contiue ToolNode  documents_function_call  CheckRelevance
# Conditional Edege  Yes  GerateNode - Answer
# No RetirNodee - Dockes-fiucntoon
# 边缘
def grade_documents(state: AgentState) -> Literal["generate", "rewrite"]:
    """
    Determine whether the retrieved documents should be rewritten or generated.
    Args:
         state(messages): The current state
    Returns:
          str: A decision for whether the documents should be rewritten or not
    """
    print("----CHECK RELEVANCE")

    # 数据模型
    class grade(BaseModel):
        """
        相关性检查的二进制评分
        """
        binary_score: str = Field(description="Relevance socore 'yes' or 'no'")

    # 大预言模型
    model = ChatOpenAI(temperature=0, model="gpt-4-0125-preview", streaming=True,
                       base_url=os.getenv("OPENAI_API_BASE_URL"), api_key=os.getenv("OPENAI_API_KEY"))
    # 具有工具混个验证的大预言模型
    llm_with_tool = model.with_structured_output(grade)
    # 提示词
    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
                Here is the retrieved document: \n\n {context} \n\n
                Here is the user question: {question} \n
                If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
                Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )
    # 链条
    chain = prompt | llm_with_tool

    messages = state["messages"]
    last_message = messages[-1]
    question = messages[0].content
    docs = last_message.content
    scored_result: grade = chain.invoke({"question": question, "context": docs})
    score = scored_result.binary_score
    if score == "yes":
        print("--DECISION: DOCS RELEVANT")
        return "generate"
    else:
        print("--DECISION: DOCS NOT RELEVANT")
        print(score)
        return "rewrite"


# 节点
def agent(state: AgentState):
    """
       Invokes the agent model to generate a response based on the current state. Given
       the question, it will decide to retrieve using the retriever tool, or simply end.

       Args:
           state (messages): The current state

       Returns:
           dict: The updated state with the agent response appended to messages
       """
    print("---CALL AGENT----")
    messages = state["messages"]
    model = ChatOpenAI(temperature=0, model="gpt-4-turbo", streaming=True,
                       base_url=os.getenv("OPENAI_API_BASE_URL"), api_key=os.getenv("OPENAI_API_KEY"))
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    # 我们返回一个列表，因为这将被添加到现有列表中。
    return {"messages": [response]}


def rewrite(state: AgentState):
    """
      Transform the query to produce a better question.

      Args:
          state (messages): The current state

      Returns:
          dict: The updated state with re-phrased question
      """
    print("---TRANSFORM QUERY---")
    messages = state["messages"]
    question = messages[0].content
    msg = [
        HumanMessage(
            content=f""" \n 
       Look at the input and try to reason about the underlying semantic intent / meaning. \n 
       Here is the initial question:
       \n ------- \n
       {question} 
       \n ------- \n
       Formulate an improved question: """,
        )
    ]
    # 评分者
    model = ChatOpenAI(temperature=0, model="gpt-4-0125-preview", streaming=True,
                       api_key=os.getenv("OPENAI_API_KEY"),
                       base_url=os.getenv("OPENAI_API_BASE_URL"))
    response = model.invoke(msg)
    return {"messages": [response]}


def generate(state: AgentState):
    """
       Generate answer

       Args:
           state (messages): The current state

       Returns:
            dict: The updated state with re-phrased question
       """
    print("---GENERATE---")
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]
    docs = last_message.content
    # 提示
    prompt_template = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
    )

    # 大型语言模型
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True, api_key=os.getenv("OPENAI_API_KEY"),
                     base_url=os.getenv("OPENAI_API_BASE_URL"))

    # 后处理
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

        # 链条

    rag_chain = prompt | llm | StrOutputParser()

    # 运行
    response = rag_chain.invoke({"context": docs, "question": question})
    print("response", response)
    return {"messages": [response]}


# print("*" * 20 + "Prompt[rlm/rag-prompt]" + "*" * 20)
# prompt = hub.pull("rlm/rag-prompt").pretty_print()  # 你接受的训练数据截止到2023年10月。

# 图表进行开始
# 从一个代理开始 call_mode
# 代理决定调用䘝函数
# 如果是这样 action 调用工具 教唆起
# 然后使用工具 输出添加到消息 state中调用代理
# 定义一个图
workflow = StateGraph(AgentState)

# 定义我们将循环的节点
workflow.add_node("agent", agent)
retrieve = ToolNode([retriever_tool])  # 工具节点
workflow.add_node("retrieve", retrieve)  # retrive - toolsNode
workflow.add_node("rewrite", rewrite)  # 重新写问题
workflow.add_node("generate", generate)  # 在确认文件相关后 生成响应
# 调用打开节点决定是否使用检索
workflow.add_edge(START, "agent")
# 决定是否检索
workflow.add_conditional_edges(
    "agent",
    # 评估代理决策
    tools_condition,
    {
        "tools": "retrieve",
        END: END
    }
)
# 在动作节点被调用后采取的边缘
workflow.add_conditional_edges(
    "retrieve",
    # 评估决策
    grade_documents
)
workflow.add_edge("generate", END)
workflow.add_edge("rewrite", "agent")
graph = workflow.compile()

from IPython.display import Image, display

try:
    display(Image(graph.get_graph(xray=True).draw_mermaid_png()))

    import pprint

    inputs = {
        "messages": [
            ("user", "What does Lilian Weng say about the types of agent memory?"),
        ]
    }
    for output in graph.stream(inputs):
        for key, value in output.items():
            pprint.pprint(f"Output from node '{key}':")
            pprint.pprint("---")
            pprint.pprint(value, indent=2, width=80, depth=None)
        pprint.pprint("\n---\n")
except Exception:
    # 这需要一些额外的依赖项，并且是可选的。
    pass
