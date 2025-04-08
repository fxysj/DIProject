from openai import OpenAI

client = OpenAI(
    base_url='https://ms-fc-21a4e8f8-d9c8.api-inference.modelscope.cn/v1',
    api_key='345c1c33-0a98-45b6-9789-68ecc0243a11', # ModelScope Token
)
response = client.chat.completions.create(
    model='unsloth/QwQ-32B-GGUF', # ModelScope Model-Id
    messages=[
        {
            'role': 'system',
            'content': 'You are a helpful assistant.'
        },
        {
            'role': 'user',
            'content': '你好'
        }
    ],
    stream=True
)
print(response)

for chunk in response:
    print(chunk.choices[0].delta.content, end='', flush=True)