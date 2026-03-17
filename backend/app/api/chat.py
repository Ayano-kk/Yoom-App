from collections.abc import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import AssistantChatRequest, AssistantChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["AI 助手模块"])


@router.post("/assistant", response_model=AssistantChatResponse, summary="AI 助手对话")
async def assistant_chat(payload: AssistantChatRequest) -> AssistantChatResponse | StreamingResponse:
    service = ChatService()
    if not payload.stream:
        return service.answer(payload)

    async def stream_generator() -> AsyncGenerator[bytes, None]:
        async for token in service.stream_answer(payload):
            yield token.encode("utf-8")

    return StreamingResponse(stream_generator(), media_type="text/plain; charset=utf-8")
