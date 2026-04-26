from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    # Database Configuration
    SQLITE_DB_PATH: str = "app.db"
    DATABASE_URL: str | None = None
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application Configuration
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # CORS Configuration
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:8000"

    @computed_field
    @property
    def sqlite_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.SQLITE_DB_PATH}"

    @computed_field
    @property
    def database_url(self) -> str:
        """Use PostgreSQL if DATABASE_URL is set, otherwise use SQLite"""
        return self.DATABASE_URL or self.sqlite_url

    @computed_field
    @property
    def allowed_origins_list(self) -> list[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
