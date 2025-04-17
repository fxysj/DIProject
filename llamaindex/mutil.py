# Multi-Modal LLMs#
# Some LLMs support multi-modal chat messages. This means that you can pass in a mix of text and other modalities (images, audio, video, etc.) and the LLM will handle it.
#
# Currently, LlamaIndex supports text, images, and audio inside ChatMessages using content blocks.
if __name__ == '__main__':
    from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
    from llama_index.llms.openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv(verbose=True)
    import os

    llm = OpenAI(model="gpt-4o",api_base=os.getenv("OPENAI_API_BASE_URL"),
                      api_key=os.getenv("OPENAI_API_KEY"))
    messages = [
        ChatMessage(
            role="user",
            blocks=[
                ImageBlock(path="image.png"),
                TextBlock(text="Describe the image in a few sentences."),
            ],
        )
    ]
    resp = llm.chat(messages)
    print(resp.message.content)