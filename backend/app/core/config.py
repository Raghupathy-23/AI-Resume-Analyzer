from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "AI Resume Analyzer API"
    api_prefix: str = "/api/v1"
    database_url: str = "mysql+pymysql://resume_user:change_me_local@localhost:3307/resume_analyzer"
    jwt_secret_key: str = "dev-only-change-this-secret"
    jwt_access_token_expire_minutes: int = 60
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    cors_origins: str = "http://localhost:5173"
    upload_dir: str = "uploads"
    max_upload_mb: int = 8
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
