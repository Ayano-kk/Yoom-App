from sqlalchemy.orm import Session, joinedload

from app.models.recommendation import Recommendation


class RecommendationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Recommendation]:
        return (
            self.db.query(Recommendation)
            .options(joinedload(Recommendation.agent))
            .order_by(Recommendation.sort_order.asc(), Recommendation.create_time.desc())
            .all()
        )

    def get_by_agent_id(self, agent_id: str) -> Recommendation | None:
        return self.db.query(Recommendation).filter(Recommendation.agent_id == agent_id).first()

    def create(self, agent_id: str, sort_order: int) -> Recommendation:
        recommendation = Recommendation(agent_id=agent_id, sort_order=sort_order)
        self.db.add(recommendation)
        self.db.flush()
        return recommendation

    def delete(self, recommendation: Recommendation) -> None:
        self.db.delete(recommendation)
        self.db.flush()
