#官方案例
# ------------------------------------------------------------------------------------
# 在 Openai官方库 中使用 DMXAPI KEY 的例子
# 需要先 pip install openai
# ------------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # 替换成你的 DMXapi 令牌key
    base_url="https://www.dmxapi.cn/v1",  # 需要改成DMXAPI的中转 https://www.dmxapi.cn/v1 ，这是已经改好的。
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "周树人和鲁迅是兄弟吗？",
        }
    ],
    model="gpt-4o-mini",    #  替换成你先想用的模型全称， 模型全称可以在DMXAPI 模型价格页面找到并复制。
)

print(chat_completion)