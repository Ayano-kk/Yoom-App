from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import PaginatedResponse


class AgentBase(BaseModel):
    agent_id: str
    agent_name: str
    agent_icon: str
    agent_desc: str
    category: str
    tags: list[str]
    status: str
    use_count: int
    is_hot: bool
    jump_url: str
    create_time: datetime


class AgentDetailResponse(AgentBase):
    model_config = {"from_attributes": True}


class AgentListResponse(PaginatedResponse):
    items: list[AgentDetailResponse] = Field(default_factory=list)
