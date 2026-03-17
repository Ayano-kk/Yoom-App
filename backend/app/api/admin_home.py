from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.recommendation import (
    RecommendationCreateRequest,
    RecommendationItem,
    RecommendationListResponse,
)
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/admin/home", tags=["运营管理模块"])


@router.get("/recommendations", response_model=RecommendationListResponse, summary="获取首页推荐列表")
def list_recommendations(db: Session = Depends(get_db)) -> RecommendationListResponse:
    return RecommendationService(db).list_recommendations()


@router.post(
    "/recommendations",
    response_model=RecommendationItem,
    status_code=status.HTTP_201_CREATED,
    summary="新增首页推荐位",
)
def create_recommendation(
    payload: RecommendationCreateRequest,
    db: Session = Depends(get_db),
) -> RecommendationItem:
    return RecommendationService(db).create_recommendation(payload)


@router.delete("/recommendations/{agent_id}", status_code=status.HTTP_204_NO_CONTENT, summary="移除推荐位")
def delete_recommendation(agent_id: str, db: Session = Depends(get_db)) -> None:
    RecommendationService(db).delete_recommendation(agent_id)
