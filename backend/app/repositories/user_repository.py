from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_openid(self, openid: str) -> User | None:
        return self.db.query(User).filter(User.wechat_openid == openid).first()

    def create(self, openid: str, nickname: str, avatar_url: str) -> User:
        user = User(wechat_openid=openid, nickname=nickname, avatar_url=avatar_url)
        self.db.add(user)
        self.db.flush()
        return user
