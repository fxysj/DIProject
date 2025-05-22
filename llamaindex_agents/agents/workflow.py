# workflow 定义
from llama_index.core.workflow import Workflow, Step
from llamaindex_agents.agents import input_agent, intent_agent, sentiment_agent, query_agent, response_agent
from llamaindex_agents.agents.events import UserInputEvent, IntentEvent, SentimentEvent, QueryEvent, ResponseEvent

conversation_workflow = Workflow(steps=[
    Step(
        name="user_input",
        fn=input_agent.handle,
        inputs=[UserInputEvent],
        outputs=[IntentEvent]
    ),
    Step(
        name="intent_detected",
        fn=intent_agent.handle,
        inputs=[IntentEvent],
        outputs=[SentimentEvent, IntentEvent]  # 支持重试，返回IntentEvent自身
    ),
    Step(
        name="sentiment_check",
        fn=sentiment_agent.handle,
        inputs=[SentimentEvent],
        outputs=[QueryEvent]
    ),
    Step(
        name="query",
        fn=query_agent.handle,
        inputs=[QueryEvent],
        outputs=[ResponseEvent]
    ),
    Step(
        name="response",
        fn=response_agent.handle,
        inputs=[ResponseEvent],
        outputs=[ResponseEvent]
    ),
])
