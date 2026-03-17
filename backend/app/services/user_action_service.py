from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_action import ActionType
from app.repositories.agent_repository import AgentRepository
from app.repositories.user_action_repository import UserActionRepository
from app.schemas.agent import AgentDetailResponse
from app.schemas.user_action import FavoriteActionRequest, FavoriteActionResponse, UserAgentListResponse


class UserActionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.agent_repository = AgentRepository(db)
        self.user_action_repository = UserActionRepository(db)

    def toggle_favorite(self, user: User, payload: FavoriteActionRequest) -> FavoriteActionResponse:
        agent = self.agent_repository.get_by_id(payload.agent_id)
        if agent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="智能体不存在")
        action = self.user_action_repository.get_action(
            user_id=user.id,
            agent_id=payload.agent_id,
            action_type=ActionType.favorite,
        )
        if payload.action == "add":
            if action is None:
                self.user_action_repository.add_action(
                    user_id=user.id,
                    agent_id=payload.agent_id,
                    action_type=ActionType.favorite,
                )
            else:
                self.user_action_repository.refresh_update_time(action)
            self._upsert_recent(user.id, payload.agent_id)
            self.db.commit()
            return FavoriteActionResponse(success=True, message="收藏成功")
        if action is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该智能体未收藏")
        self.user_action_repository.remove_action(action)
        self.db.commit()
        return FavoriteActionResponse(success=True, message="已取消收藏")

    def list_favorites(self, user: User) -> UserAgentListResponse:
        agents = self.user_action_repository.list_agents_by_action(user.id, ActionType.favorite)
        return UserAgentListResponse(items=[AgentDetailResponse.model_validate(item) for item in agents])

    def list_recent(self, user: User) -> UserAgentListResponse:
        agents = self.user_action_repository.list_agents_by_action(user.id, ActionType.recent)
        return UserAgentListResponse(items=[AgentDetailResponse.model_validate(item) for item in agents])

    def _upsert_recent(self, user_id: int, agent_id: str) -> None:
        recent_action = self.user_action_repository.get_action(user_id, agent_id, ActionType.recent)
        if recent_action is None:
            self.user_action_repository.add_action(
                user_id=user_id,
                agent_id=agent_id,
                action_type=ActionType.recent,
            )
            return
        self.user_action_repository.refresh_update_time(recent_action)
