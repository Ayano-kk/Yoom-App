from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import get_optional_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.agent import AgentDetailResponse, AgentListResponse
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agents", tags=["智能体模块"])


@router.get("/", response_model=AgentListResponse, summary="获取智能体分页列表")
def list_agents(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    category: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> AgentListResponse:
    return AgentService(db).list_agents(page=page, size=size, category=category, keyword=keyword)


@router.get("/{agent_id}", response_model=AgentDetailResponse, summary="获取智能体详情")
def get_agent_detail(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
) -> AgentDetailResponse:
    return AgentService(db).get_agent_detail(agent_id=agent_id, current_user=current_user)
