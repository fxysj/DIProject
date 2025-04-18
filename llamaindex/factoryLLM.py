from dotenv import load_dotenv
load_dotenv(verbose=True)
import os
from llama_index.llms.openai import OpenAI
def factoryLLM():
    llm = OpenAI(model="gpt-4o", api_base=os.getenv("OPENAI_API_BASE_URL"),
                 api_key=os.getenv("OPENAI_API_KEY"))
    return llm