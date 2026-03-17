from sqlalchemy.orm import Session

from app.models.agent import Agent
from app.models.user_action import ActionType, UserAction


class UserActionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_action(self, user_id: int, agent_id: str, action_type: ActionType) -> UserAction | None:
        return (
            self.db.query(UserAction)
            .filter(
                UserAction.user_id == user_id,
                UserAction.agent_id == agent_id,
                UserAction.action_type == action_type,
            )
            .first()
        )

    def add_action(self, user_id: int, agent_id: str, action_type: ActionType) -> UserAction:
        action = UserAction(user_id=user_id, agent_id=agent_id, action_type=action_type)
        self.db.add(action)
        self.db.flush()
        return action

    def remove_action(self, action: UserAction) -> None:
        self.db.delete(action)
        self.db.flush()

    def refresh_update_time(self, action: UserAction) -> UserAction:
        self.db.add(action)
        self.db.flush()
        self.db.refresh(action)
        return action

    def list_agents_by_action(self, user_id: int, action_type: ActionType) -> list[Agent]:
        return (
            self.db.query(Agent)
            .join(UserAction, UserAction.agent_id == Agent.agent_id)
            .filter(UserAction.user_id == user_id, UserAction.action_type == action_type)
            .order_by(UserAction.update_time.desc())
            .all()
        )
