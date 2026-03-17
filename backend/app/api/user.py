from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user_action import FavoriteActionRequest, FavoriteActionResponse, UserAgentListResponse
from app.services.user_action_service import UserActionService

router = APIRouter(prefix="/user", tags=["用户行为模块"])


@router.post("/favorites", response_model=FavoriteActionResponse, summary="收藏或取消收藏智能体")
def toggle_favorite(
    payload: FavoriteActionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FavoriteActionResponse:
    return UserActionService(db).toggle_favorite(current_user, payload)


@router.get("/favorites", response_model=UserAgentListResponse, summary="获取当前用户收藏列表")
def list_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserAgentListResponse:
    return UserActionService(db).list_favorites(current_user)


@router.get("/recent", response_model=UserAgentListResponse, summary="获取最近使用记录")
def list_recent(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserAgentListResponse:
    return UserActionService(db).list_recent(current_user)
