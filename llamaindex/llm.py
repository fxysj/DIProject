import asyncio
import os

from llama_index.core.base.llms.types import ChatMessage
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
load_dotenv(verbose=True)
import os

async def main():
    llm=  OpenAI(api_base=os.getenv("OPENAI_API_BASE_URL"),
                      api_key=os.getenv("OPENAI_API_KEY")
                      )
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content="Tell me a joke."),
    ]
    chat_response = llm.chat(messages)
    print(chat_response)

    llm = OpenAI(model="gpt-4o-mini",api_base=os.getenv("OPENAI_API_BASE_URL"),
                      api_key=os.getenv("OPENAI_API_KEY"))
    response = llm.complete("Who is Laurie Voss?")
    print(response)
    # for token in handle:
    #     print(token.delta, end="", flush=True)



if __name__ == '__main__':
    asyncio.run(main())