from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "沄荣科技智能体后端"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./wechatapp.db"
    jwt_secret_key: str = "yunrong-tech-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
