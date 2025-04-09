from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config import OPENAI_API_KEY, OPENAI_BASE_URL

available_tools = {
    "calculate_bmi": "计算BMI",
    "translate_text": "翻译文本",
    "generate_image": "生成图片",
}

tool_list_text = "\n".join([f"- {k}：{v}" for k, v in available_tools.items()])
prompt_text = f"""你是一个智能意图识别助手。请根据用户的提问内容，从以下意图中选择一个最匹配的：
{tool_list_text}
用户说：{{query}}
请只返回意图关键词（如 calculate_bmi），不要添加其他文字。"""

llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
intent_prompt = ChatPromptTemplate.from_template(prompt_text)
intent_runnable = intent_prompt | llm | (lambda x: {"intent": x.content.strip()})
