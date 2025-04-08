import os

from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import json
from textwrap import dedent
#加载环境变量 例如 API key 等配置信息
load_dotenv()
#设置Openai API 工厂名称 默认为openai
factory = "openai"
#初始化OpenaAI客户端 传入key base URL
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL"),
)
#定义一个产品信息类 用于解析API返回的数据
class ProductInfo(BaseModel):
    product_name:str #产品的名称 字符串类型
    price:float #价格浮点数类型
    description:str #产品的描述 字符串类型
#定义一个提示信息 用于请求模型返回JSON格式的产品信息
product_prompt = '''
根据给出的产品进行分析,按json格式用中文回答,json format:product_name,price,description.
'''
#获取产品信息的函数 传入用户的问题
def get_product_info(question: str):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": dedent(product_prompt)},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content
    # 返回模型解析的第一个选项的消息结果
    #return completion.choices[0].message.parsed



# 定义将解析的结果转换为 JSON 的函数
def transform2JSON(parsed_result):
    # print(parsed_result)  # 打印解析结果

    # 将解析的结果存储到字典中
    product_inform["product_name"] = parsed_result.product_name
    product_inform["price"] = parsed_result.price
    product_inform["description"] = parsed_result.description

    # 将字典转换为 JSON 字符串并返回，ensure_ascii=False 允许中文字符正常显示
    return json.dumps(product_inform, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # 初始化一个空的产品信息字典
    product_inform = {}
    # 定义用户输入的问题，即一个产品信息的描述
    question = "75寸小米电视机"

    # 调用函数获取产品信息
    result = get_product_info(question)
    print(result)

    # 将解析结果转换为 JSON 格式并打印
    # json_result = transform2JSON(result)
    # print(json_result)

