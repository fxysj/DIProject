from langchain_core.beta.runnables.context import Context
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import PromptTemplate
def FakeListLLM(p):
    print(p)
    return "hello"
chain = (
    Context.setter("input")
    |{
    "context":RunnablePassthrough()
             |Context.setter("context"),
    "question":RunnablePassthrough(),
    }
    |PromptTemplate.from_template("""{context} {question}""")
    |FakeListLLM
    |StrOutputParser()
    |{
      "result":RunnablePassthrough(),
      "context":Context.getter("context"),
      "input":Context.getter("input"),
    }
)
out = chain.invoke("what is name")
print(out)

#对用户的问题进行填充和完整丰富返回
def accirequeInput(input:str):
    print("获取到了用户的输入信息:")
    print(input)
    return "获取到了用户输入信息:"+input
def LLMAccTIRUT(templateStr:str):
    return "大模型返回"

#定义一个函数链
#信息-context进行保存
#保存玩之后再次传递到accireinput里面
#return 信息
chain2 = (
    Context.setter("input")| # 进行保存用户的信息
    accirequeInput|
    {
        "inputFill":RunnablePassthrough()|Context.setter("inputFill")#获取到对应的填充完整的数据
    }
    |PromptTemplate.from_template("""{inputFill}""")|Context.setter("temp")
    |LLMAccTIRUT
    |StrOutputParser()
    |{
    "result":RunnablePassthrough(),
    "inputFill":Context.getter("inputFill"),
    "tem":Context.getter("temp"),
    }
)
out = chain2.invoke("ni hao ")
print(out)