from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.agent import Agent


class AgentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, agent_id: str) -> Agent | None:
        return self.db.query(Agent).filter(Agent.agent_id == agent_id).first()

    def list_paginated(
        self,
        page: int,
        size: int,
        category: str | None = None,
        keyword: str | None = None,
    ) -> tuple[list[Agent], int]:
        query = self.db.query(Agent)
        if category:
            query = query.filter(Agent.category == category)
        if keyword:
            fuzzy = f"%{keyword}%"
            query = query.filter(or_(Agent.agent_name.ilike(fuzzy), Agent.agent_desc.ilike(fuzzy)))
        total = query.count()
        items = (
            query.order_by(Agent.is_hot.desc(), Agent.use_count.desc(), Agent.create_time.desc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
        return items, total

    def increase_use_count(self, agent: Agent) -> Agent:
        agent.use_count += 1
        self.db.flush()
        return agent
