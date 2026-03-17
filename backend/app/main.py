from fastapi import FastAPI

from app.api.admin_home import router as admin_home_router
from app.api.agents import router as agents_router
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.user import router as user_router
from app.core.config import settings
from app.db.session import engine
from app.models.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)

app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(agents_router, prefix=settings.api_prefix)
app.include_router(user_router, prefix=settings.api_prefix)
app.include_router(admin_home_router, prefix=settings.api_prefix)
app.include_router(chat_router, prefix=settings.api_prefix)


@app.get("/", summary="服务健康检查")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
