from langchain_anthropic import ChatAnthropic
from langchain_core.runnables.utils import ConfigurableField
from langchain_openai import ChatOpenAI
OPENAI_API_KEY="sk-3GiWozbrq1kFipcgF7ymSbgH9g1f5lWGfpkUgfWBICul0Kai"
OPENAI_API_BASE_URL="https://www.dmxapi.cn/v1"

model = ChatAnthropic(
    model_name="claude-3-5-sonnet-20240620",
    base_url=OPENAI_API_BASE_URL,
    api_key=OPENAI_API_KEY,
).configurable_alternatives(
    ConfigurableField(id="llm"),
    openai=ChatOpenAI(model="gpt-4o",base_url=OPENAI_API_BASE_URL,api_key=OPENAI_API_KEY),
    ce=ChatOpenAI(model="gpt-4o",base_url=OPENAI_API_BASE_URL,api_key=OPENAI_API_KEY)
)
#也就是可以进行定义一个标准的模型
#然后将配置信息放到 llm:进行配置中心完成中心配置
#可以自定义去设置环境的配置
#可以自定义事件驱动
#可以自定义模型配置
#chain Runnabel RunnConfig

# uses the default model ChatAnthropic
#print(model.invoke("which organization created you?").content)
#上面
# uses ChatOpenAI
print(
    model.with_config(
        configurable={"llm": "ce"}
    ).invoke("which organization created you?").content
)