import hashlib

from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)

    def login(self, payload: LoginRequest) -> LoginResponse:
        openid = self._mock_get_openid(payload.code)
        user = self.user_repository.get_by_openid(openid)
        if user is None:
            user = self.user_repository.create(
                openid=openid,
                nickname=payload.nickname,
                avatar_url=payload.avatar_url,
            )
        else:
            user.nickname = payload.nickname
            user.avatar_url = payload.avatar_url
        self.db.commit()
        token = create_access_token(subject=str(user.id))
        return LoginResponse(access_token=token)

    @staticmethod
    def _mock_get_openid(code: str) -> str:
        digest = hashlib.sha256(code.encode("utf-8")).hexdigest()
        return f"wx_{digest[:24]}"
