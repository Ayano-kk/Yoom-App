from pydantic import BaseModel, Field

from app.schemas.agent import AgentDetailResponse


class FavoriteActionRequest(BaseModel):
    agent_id: str = Field(..., min_length=1, max_length=64)
    action: str = Field(..., pattern="^(add|remove)$")


class FavoriteActionResponse(BaseModel):
    success: bool
    message: str


class UserAgentListResponse(BaseModel):
    items: list[AgentDetailResponse]
