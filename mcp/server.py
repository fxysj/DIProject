from datetime import datetime
import glob
import json
import os
from typing import List
from mcp import Resource
from mcp.server.fastmcp import FastMCP
from mcp.types import  Resource,TextContent,EmbeddedResource
from exa_py import Exa
#初始化FastMCP 服务器
mcp = FastMCP("qwen-docs-server")
#定义文档目录常量
DOCS_DIR = "./qwen_resource"
RESULT_DIR = "./log"
# 确保结果目录存在
os.makedirs(RESULT_DIR, exist_ok=True)
# Exa API 密钥
EXA_API_KEY = "23703469-b9fd-4281-8c84-7a05714f3d5a"


# ===== 资源定义函数 =====

@mcp.resource("qwen-doc://qwen1.5.md", description="Qwen documentation: qwen1.5.md")
def get_qwen15_doc() -> str:
    """获取 Qwen1.5 的文档内容

    返回：
        str: Qwen1.5 文档的内容
    """
    file_path = os.path.join(DOCS_DIR, "Qwen1.5.md")
    return _read_file_content(file_path)


@mcp.resource("qwen-doc://qwen2.md", description="Qwen documentation: qwen2.md")
def get_qwen2_doc() -> str:
    """获取 Qwen2 的文档内容

    返回：
        str: Qwen2 文档的内容
    """
    file_path = os.path.join(DOCS_DIR, "Qwen2.md")
    return _read_file_content(file_path)


@mcp.tool(description="保存问题和回答到本地文件")
def save_to_local(file_name: str, question: str, answer: str) -> str:
    """将问题和回答保存到本地文件

    参数：
        file_name: 保存的文件名
        question: 用户的问题
        answer: 回答内容

    返回：
        str: 保存成功的消息
    """
    data = {
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    }

    file_path = os.path.join(RESULT_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return f"成功保存到: {file_path}"


@mcp.tool(description="通过 Exa 搜索 API 查询问题")
def request_exa(question: str) -> str:
    """使用 Exa 搜索 API 查询问题的相关内容

    参数：
        question: 要搜索的问题

    返回：
        str: 搜索结果或错误信息
    """
    try:
        # 初始化 Exa 客户端
        exa = Exa(api_key=EXA_API_KEY)

        # 发送 API 请求
        search_results = exa.search_and_contents(
            question,
            text={"max_characters": 1000}
        )

        # 格式化结果
        formatted_results = []
        for index, result in enumerate(search_results.results):
            formatted_results.append(
                f"title {index}: {result.title} content {index}: " + result.text.replace('\n', '')
            )

        return '\n\n'.join(formatted_results)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# ===== 提示模板 =====

@mcp.prompt(description="简洁回答的提示模板")
def simple_reply(question: str) -> str:
    """生成简洁回答的提示模板

    参数：
        question: 用户问题

    返回：
        str: 提示模板文本
    """
    return f"请简洁地回答以下问题:\n\n{question}"


@mcp.prompt(description="详细回答的提示模板")
def detailed_response(question: str) -> str:
    """生成详细回答的提示模板

    参数：
        question: 用户问题

    返回：
        str: 提示模板文本
    """
    return f"请详细回答以下问题:\n\n{question}"


# ===== 辅助函数 =====

def _read_file_content(file_path: str) -> str:
    """读取文件内容的辅助函数

    参数：
        file_path: 文件路径

    返回：
        str: 文件内容
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"读取文件 {file_path} 失败: {str(e)}"
# ===== 主程序入口 =====

if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')