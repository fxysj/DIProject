# config.py
import os
from dotenv import load_dotenv

# 加载项目根目录下的 .env 文件
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

if not OPENAI_API_KEY:
    raise ValueError("请在 .env 文件中配置 OPENAI_API_KEY")
if not OPENAI_BASE_URL:
    raise ValueError("请在 .env 文件中配置 OPENAI_BASE_URL")
