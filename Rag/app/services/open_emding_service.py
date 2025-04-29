#openAIEmbingds服务
from langchain_openai import OpenAIEmbeddings
OPENAI_API_KEY="sk-3GiWozbrq1kFipcgF7ymSbgH9g1f5lWGfpkUgfWBICul0Kai"
OPENAI_API_BASE_URL="https://www.dmxapi.cn/v1"
embedder = OpenAIEmbeddings(
    model="text-embedding-3-large",
    max_retries=2,
    base_url=OPENAI_API_BASE_URL,
    api_key=OPENAI_API_KEY,
)
# input_text = "The meaning of life is 42"
# vector = embedder.embed_query("hello")
# print(vector[:3])


# Embed multiple texts:
vectors = embedder.embed_documents(["hello", "goodbye"])
# Showing only the first 3 coordinates
print(len(vectors))