# 查询引擎代码，封装 LlamaIndex 索引加载和查询
# query_engine.py
import os
from llama_index import download_loader, GPTVectorStoreIndex, StorageContext, load_index_from_storage

# 文档目录
DOCS_DIR = "docs"
# 索引存储目录
INDEX_DIR = "index_storage"

def build_index() -> GPTVectorStoreIndex:
    """构建索引并持久化"""
    print("[QueryEngine] 创建新索引...")
    # 加载文本加载器
    SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
    loader = SimpleDirectoryReader(DOCS_DIR)
    documents = loader.load_data()

    # 构建索引
    index = GPTVectorStoreIndex.from_documents(documents)

    # 保存索引到本地
    index.storage_context.persist(persist_dir=INDEX_DIR)
    return index

def load_index() -> GPTVectorStoreIndex:
    """加载已有索引，如果没有则构建"""
    if os.path.exists(INDEX_DIR):
        print("[QueryEngine] 从存储加载索引...")
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        index = load_index_from_storage(storage_context)
        return index
    else:
        return build_index()

index = load_index()

def query_index(query_text: str) -> str:
    """根据查询文本返回索引回答"""
    response = index.query(query_text)
    return str(response)


