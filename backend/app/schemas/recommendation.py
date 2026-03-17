from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.agent import AgentDetailResponse


class RecommendationCreateRequest(BaseModel):
    agent_id: str = Field(..., min_length=1, max_length=64)
    sort_order: int = Field(default=0, ge=0, le=9999)


class RecommendationItem(BaseModel):
    id: int
    sort_order: int
    create_time: datetime
    agent: AgentDetailResponse

    model_config = {"from_attributes": True}


class RecommendationListResponse(BaseModel):
    items: list[RecommendationItem]
