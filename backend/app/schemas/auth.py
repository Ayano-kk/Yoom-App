from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=128)
    nickname: str = Field(default="微信用户", max_length=64)
    avatar_url: str = Field(default="", max_length=255)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
