import asyncio

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import (
    InputRequiredEvent,
    HumanResponseEvent, Context,
)

from llamaindex.factoryLLM import factoryLLM


#为了让人类参与进来 我们将让工具发出一个在工作流中其他步骤都未收到的事件
#然后我们会告诉工具等待 直到它收到一个特定的回复事件
#我们内置了InputRequiredEvent 和HumanResponseEvent 事件实现此目的
#如果您想捕获不同形式的人工输入 可以根据自己的偏好对这些事件进行子类化
#让我们导入他们
#接下来我们将创建一个执行危险任务的工具 这里有一些新的东西
#wait_for_event 用于等待HumanResponseEvent
#这waiter_event是写入事件流的事件,以便于让调用者知道我们正在等待响应
#waiter_id 是此特定等待调用的唯一标识符 它有助于确保我们waiter_event 每次只发送一个waiter_id
#该requirements参数用于指定我们要等待具有特定的HumanResponseEvent user_name
async def dangerous_task(ctx:Context)->str:
    """A dangerous task that requires human confirmation"""
    #emit a waiter event (InputRequiredEvent)
    #and wait until we see a HumanResponseEvent
    question = "Are you sure you want to proceed? "
    response = await ctx.wait_for_event(
        HumanResponseEvent,
        waiter_id=question,
        waiter_event=InputRequiredEvent(
            prefix=question,
            user_name="Laurie",
        ),
        requirements={"user_name":"Laurie"}
    )
    # act on the input from the event
    if response.response.strip().lower() == "yes":
        return "Dangerous task completed successfully."
    else:
        return "Dangerous task aborted."

workflow = FunctionAgent(
    tools=[dangerous_task],
    llm=factoryLLM(),
    system_prompt="You are a helpful assistant that can perform dangerous tasks.",
)
async def main():
    handler = workflow.run(user_msg="I want to proceed with the dangerous task.")

    async for event in handler.stream_events():
        if isinstance(event, InputRequiredEvent):
            # capture keyboard input
            response = input(event.prefix)
            # send our response back
            handler.ctx.send_event(
                HumanResponseEvent(
                    response=response,
                    user_name=event.user_name,
                )
            )

    response = await handler
    print(str(response))

if __name__ == '__main__':
    asyncio.run(main())