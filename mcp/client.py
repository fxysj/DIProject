
import asyncio
import os
import sys
from contextlib import AsyncExitStack
from typing import Optional, List, Dict

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, stdio_client
from openai import OpenAI
load_dotenv()

class MCPClient:
    """MCP客户端，用于与OpenAI API交互并调用MCP工具"""

    def __init__(self):
        """初始化MCP客户端"""
        # 环境变量检查和初始化
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("BASE_URL")
        self.model = os.getenv("MODEL")

        if not self.openai_api_key:
            raise ValueError(
                "❌ 未找到OpenAI API Key，请在.env文件中设置OPENAI_API_KEY"
            )

        # 初始化组件
        self.exit_stack = AsyncExitStack()
        self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url)
        self.session: Optional[ClientSession] = None
        self.resources_dict = {}

    async def connect_to_server(self, server_script_path: str):
        """连接到MCP服务器并初始化会话"""
        # 检查脚本类型
        if server_script_path.endswith(".py"):
            command = "python"
        elif server_script_path.endswith(".js"):
            command = "node"
        else:
            raise ValueError("服务器脚本必须是.py或.js文件")

        # 设置服务器参数并建立连接
        server_params = StdioServerParameters(
            command=command, args=[server_script_path], env=None
        )

        # 初始化连接和会话
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )
        await self.session.initialize()

        # 加载服务器工具和资源
        await self._load_tools_and_resources()

    async def _load_tools_and_resources(self):
        """加载服务器上的工具和资源"""
        # 加载工具
        tools_response = await self.session.list_tools()
        tools = tools_response.tools
        print(f"\n已连接到服务器，支持以下工具: {[tool.name for tool in tools]}")

        # 加载资源
        resources_response = await self.session.list_resources()
        resources_names = [resource.name for resource in resources_response.resources]

        # 读取所有资源内容
        for resource_name in resources_names:
            resource = await self.session.read_resource(resource_name)
            self.resources_dict[resource_name] = resource.contents[0].text

    async def select_prompt_template(self, user_question: str) -> str:
        """根据用户问题选择合适的提示模板"""
        # 需要详细回答的指示词
        detailed_indicators = [
            "解释", "说明", "详细", "具体", "详尽", "深入", "全面", "彻底",
            "分析", "为什么", "怎么样", "如何", "原因", "机制", "过程",
            "explain", "detail", "elaborate", "comprehensive", "thorough",
            "in-depth", "analysis", "why", "how does", "reasons",
            "背景", "历史", "发展", "比较", "区别", "联系", "影响", "意义",
            "优缺点", "利弊", "方法", "步骤", "案例", "举例", "证明",
            "理论", "原理", "依据", "论证", "详解", "指南", "教程",
            "细节", "要点", "关键", "系统", "完整", "清晰", "请详细"
        ]

        # 判断问题类型
        question_lower = user_question.lower()
        is_brief_question = len(question_lower.split()) < 10
        wants_details = any(
            indicator in question_lower for indicator in detailed_indicators
        )

        # 返回模板类型
        return (
            "detailed_response"
            if (wants_details or not is_brief_question)
            else "simply_replay"
        )

    async def transform_json(self, tools_data: List[Dict]) -> List[Dict]:
        """将Claude Function calling格式转换为OpenAI格式"""
        result = []

        for item in tools_data:
            old_func = item["function"]

            # 构建新的function对象
            new_func = {
                "name": old_func["name"],
                "description": old_func["description"],
                "parameters": {},
            }

            # 转换input_schema为parameters
            if "input_schema" in old_func and isinstance(
                old_func["input_schema"], dict
            ):
                schema = old_func["input_schema"]
                new_func["parameters"] = {
                    "type": schema.get("type", "object"),
                    "properties": schema.get("properties", {}),
                    "required": schema.get("required", []),
                }

            result.append({"type": item["type"], "function": new_func})

        return result

    async def add_relevant_resources(self, user_question: str) -> str:
        """根据用户问题添加相关资源到上下文"""
        # 关键词与资源映射
        keywords_map = {
            "qwen1.5": ["qwen-doc://qwen1.5.md"],
            "qwen2": ["qwen-doc://qwen2.md"],
            "千问": ["qwen-doc://qwen1.5.md", "qwen-doc://qwen2.md"],
        }

        # 查找匹配的资源
        matched_resources = []
        for keyword, resources in keywords_map.items():
            if keyword in user_question:
                for resource in resources:
                    if (
                        resource in self.resources_dict
                        and resource not in matched_resources
                    ):
                        matched_resources.append(resource)

        # 没有匹配则返回原问题
        if not matched_resources:
            return user_question

        # 构建增强的问题
        context_parts = []
        for resource in matched_resources:
            context_parts.append(f"--- {resource} ---\n{self.resources_dict[resource]}")

        return (
            user_question + "\n\n相关信息:\n\n" + "\n\n".join(context_parts)
        )

    async def process_query(self, query: str) -> str:
        """处理用户查询并调用必要的工具"""
        if not self.session:
            return "❌ 未连接到MCP服务器"

        try:
            # 1. 获取可用工具
            tools_response = await self.session.list_tools()
            tools_data = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema,
                    },
                }
                for tool in tools_response.tools
            ]

            # 2. 转换工具格式
            available_tools = await self.transform_json(tools_data)

            # 3. 选择提示模板并应用
            template_name = await self.select_prompt_template(query)
            prompt_response = await self.session.get_prompt(
                template_name, arguments={"question": query}
            )
            prompt_text = prompt_response.messages[0].content.text
            print("\n[使用提示模板: ", template_name, "], 提示内容: ", prompt_text, "]")

            # 4. 添加相关资源
            enriched_prompt = await self.add_relevant_resources(prompt_text)
            print(enriched_prompt)

            # 5. 发送请求到OpenAI
            messages = [{"role": "user", "content": enriched_prompt}]
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, tools=available_tools
            )

            # 6. 处理工具调用
            max_tool_calls = 5  # 限制工具调用次数
            call_count = 0

            while (
                response.choices[0].message.tool_calls and call_count < max_tool_calls
            ):
                tool_call = response.choices[0].message.tool_calls[0]
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # 调用工具
                print(f"\n[正在调用工具 {tool_name}, 参数: {tool_args}]")
                result = await self.session.call_tool(tool_name, tool_args)

                # 更新消息历史
                messages.append(response.choices[0].message.model_dump())
                messages.append(
                    {
                        "role": "tool",
                        "content": result.content[0].text,
                        "tool_call_id": tool_call.id,
                    }
                )

                # 再次请求OpenAI
                response = self.client.chat.completions.create(
                    model=self.model, messages=messages, tools=available_tools
                )

                call_count += 1

            # 7. 返回最终结果
            return response.choices[0].message.content

        except Exception as e:
            return f"❌ 处理查询时出错: {str(e)}"

    async def chat_loop(self):
        """运行交互式聊天循环"""
        print("\n  MCP客户端已启动！输入'quit'退出")

        while True:
            try:
                query = input("\n你: ").strip()
                if query.lower() == "quit":
                    break

                print("\n  处理中...")
                response = await self.process_query(query)
                print(f"\n  回复: {response}")

            except KeyboardInterrupt:
                print("\n\n  已终止会话")
                break
            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")

    async def cleanup(self):
        """清理资源"""
        if self.exit_stack:
            await self.exit_stack.aclose()
            print("\n  已清理资源并断开连接")


async def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python client.py <服务器脚本路径>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    except Exception as e:
        print(f"\n⚠️ 程序出错: {str(e)}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())