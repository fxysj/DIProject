# FastAPI入口
from fastapi import FastAPI
from pydantic import BaseModel
from agents.workflow import conversation_workflow
from agents.events import UserInputEvent, ResponseEvent, IntentEvent

app = FastAPI()

class UserRequest(BaseModel):
    text: str

@app.post("/chat")
async def chat(request: UserRequest):
    input_event = UserInputEvent(text=request.text)
    result_event = await conversation_workflow.arun(input_event)

    # 如果是ResponseEvent且有消息返回
    if isinstance(result_event, ResponseEvent) and result_event.message:
        return {"response": result_event.message}

    # 如果是IntentEvent且意图未知，提示重试
    if isinstance(result_event, IntentEvent) and result_event.intent == "未知":
        return {"response": "抱歉，没理解您的意图，请再说一遍。"}

    # 兜底
    return {"response": "系统异常，请稍后重试。"}
