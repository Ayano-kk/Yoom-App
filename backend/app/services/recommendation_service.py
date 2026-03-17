from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.agent_repository import AgentRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.schemas.agent import AgentDetailResponse
from app.schemas.recommendation import (
    RecommendationCreateRequest,
    RecommendationItem,
    RecommendationListResponse,
)


class RecommendationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.agent_repository = AgentRepository(db)
        self.recommendation_repository = RecommendationRepository(db)

    def list_recommendations(self) -> RecommendationListResponse:
        items = self.recommendation_repository.list_all()
        serialized = [
            RecommendationItem(
                id=item.id,
                sort_order=item.sort_order,
                create_time=item.create_time,
                agent=AgentDetailResponse.model_validate(item.agent),
            )
            for item in items
        ]
        return RecommendationListResponse(items=serialized)

    def create_recommendation(self, payload: RecommendationCreateRequest) -> RecommendationItem:
        agent = self.agent_repository.get_by_id(payload.agent_id)
        if agent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="智能体不存在")
        exists = self.recommendation_repository.get_by_agent_id(payload.agent_id)
        if exists is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="推荐位已存在该智能体")
        recommendation = self.recommendation_repository.create(
            agent_id=payload.agent_id,
            sort_order=payload.sort_order,
        )
        self.db.commit()
        self.db.refresh(recommendation)
        return RecommendationItem(
            id=recommendation.id,
            sort_order=recommendation.sort_order,
            create_time=recommendation.create_time,
            agent=AgentDetailResponse.model_validate(agent),
        )

    def delete_recommendation(self, agent_id: str) -> None:
        recommendation = self.recommendation_repository.get_by_agent_id(agent_id)
        if recommendation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="推荐位不存在")
        self.recommendation_repository.delete(recommendation)
        self.db.commit()
