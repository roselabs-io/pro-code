from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://blog:blog@localhost:5432/blog"
    jwt_secret: str = "dev-insecure-change-me-min-32-bytes-long"
    jwt_alg: str = "HS256"
    access_token_ttl_seconds: int = 3600
    site_url: str = "http://localhost:8080"


settings = Settings()
