import asyncio
from collections.abc import AsyncGenerator

from app.schemas.chat import AssistantChatRequest, AssistantChatResponse


class ChatService:
    def answer(self, payload: AssistantChatRequest) -> AssistantChatResponse:
        normalized = payload.message.strip()
        answer = f"我是沄荣科技 AI 助手，已收到你的问题：{normalized}。建议先明确业务目标，再拆解数据与流程。"
        return AssistantChatResponse(answer=answer)

    async def stream_answer(self, payload: AssistantChatRequest) -> AsyncGenerator[str, None]:
        answer = self.answer(payload).answer
        for token in answer:
            yield token
            await asyncio.sleep(0.02)
