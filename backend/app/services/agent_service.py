from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_action import ActionType
from app.repositories.agent_repository import AgentRepository
from app.repositories.user_action_repository import UserActionRepository
from app.schemas.agent import AgentDetailResponse, AgentListResponse


class AgentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.agent_repository = AgentRepository(db)
        self.user_action_repository = UserActionRepository(db)

    def list_agents(
        self,
        page: int,
        size: int,
        category: str | None = None,
        keyword: str | None = None,
    ) -> AgentListResponse:
        items, total = self.agent_repository.list_paginated(
            page=page,
            size=size,
            category=category,
            keyword=keyword,
        )
        return AgentListResponse(
            page=page,
            size=size,
            total=total,
            items=[AgentDetailResponse.model_validate(item) for item in items],
        )

    def get_agent_detail(self, agent_id: str, current_user: User | None = None) -> AgentDetailResponse:
        agent = self.agent_repository.get_by_id(agent_id)
        if agent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="智能体不存在")
        if current_user:
            action = self.user_action_repository.get_action(
                user_id=current_user.id,
                agent_id=agent_id,
                action_type=ActionType.recent,
            )
            if action is None:
                self.user_action_repository.add_action(
                    user_id=current_user.id,
                    agent_id=agent_id,
                    action_type=ActionType.recent,
                )
            else:
                self.user_action_repository.refresh_update_time(action)
            self.agent_repository.increase_use_count(agent)
            self.db.commit()
        return AgentDetailResponse.model_validate(agent)
