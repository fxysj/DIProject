import uuid

from langgraph.types import Command

from langgraph.services.mutil_interput_service import graph
if __name__ == '__main__':
    thread_config = {"configurable": {"thread_id": uuid.uuid4()}}
    inputs = [
        # 第一轮对话，
        {
            "messages":
                [
                {"role": "user", "content": "i wanna go somewhere warm in the caribbean"}
            ]
        },
    # Since we're using `interrupt`, we'll need to resume using the Command primitive.
        # 第二轮对话，
        Command(
            resume="could you recommend a nice hotel in one of the areas and tell me which area it is."
        ),
        # 第三轮对话，
        Command(resume="could you recommend something to do near the hotel?"),
    ]

    for idx, user_input in enumerate(inputs):
        print()
        print(f"--- Conversation Turn {idx + 1} ---")
        print()
        print(f"User: {user_input}")
        print()
        for update in graph.stream(
                user_input,
                config=thread_config,
                stream_mode="updates",
        ):
            for node_id, value in update.items():
                if isinstance(value, dict) and value.get("messages", []):
                    last_message = value["messages"][-1]
                    if last_message["role"] != "ai":
                        continue
                    print(f"{last_message['name']}: {last_message['content']}")






