from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio
from services.agent_service import process_user_message

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str
    data: Dict[str, Any] = {}

class UserRequest(BaseModel):
    id: str
    messages: List[Message]
    session_id: str

@app.post("/chat/stream")
async def chat_stream(request: UserRequest):
    async def event_stream():
        async for chunk in process_user_message(request):
            yield chunk
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.post("/chat/analysis")
async def chat_analysis(request: UserRequest):
    result = await process_user_message(request, stream=False)
    return JSONResponse(content=result) 