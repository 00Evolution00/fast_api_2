from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    # Database Configuration
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "fastapi_db"
    POSTGRES_USER: str = "fastapi_user"
    POSTGRES_PASSWORD: str = "fastapi_password"
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
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def database_url(self) -> str:
        return self.DATABASE_URL or self.postgres_url

    @computed_field
    @property
    def allowed_origins_list(self) -> list[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
