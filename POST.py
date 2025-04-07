import os

from dotenv import load_dotenv
load_dotenv()
import requests
import json
# ------------------------------------------------------------------------------------
#         3秒步接入 DMXAPI ：  修改 Key 和 Base url (https://www.dmxapi.cn)
# ----------------------------------------------------------------------------------
url = "https://openrouter.ai/api/v1/chat/completions"   # 这里不要用 openai base url，需要改成DMXAPI的中转 https://www.dmxapi.cn ，下面是已经改好的
payload = json.dumps({
     "model": "gpt-4o-mini",  # 这里是你需要访问的模型，改成上面你需要测试的模型名称就可以了。
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "周树人和鲁迅是兄弟吗？"
        }
    ]
})
headers = {
   'Accept': 'application/json',
   'Authorization': os.getenv("OPENAI_API_KEY"), # 这里放你的 DMXapi key
   'User-Agent': 'DMXAPI/1.0.0 (https://www.dmxapi.cn)',  # 这里也改成 DMXAPI 的中转URL https://www.dmxapi.cn，已经改好
   'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)