from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Agent(Base):
    __tablename__ = "agents"

    agent_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    agent_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    agent_icon: Mapped[str] = mapped_column(String(255), nullable=False)
    agent_desc: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="online")
    use_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_hot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    jump_url: Mapped[str] = mapped_column(String(255), nullable=False)
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    actions = relationship("UserAction", back_populates="agent")
    recommendations = relationship("Recommendation", back_populates="agent")
