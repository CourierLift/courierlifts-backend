
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    SECRET_KEY: str = "change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    DATABASE_URL: str = "sqlite:///./courierlifts.db"
    OPENWEATHER_API_KEY: str | None = None

    # CORS
    ALLOW_ORIGINS: List[str] = ["*"]  # replace with ["https://courierlifts.com"] in prod

    class Config:
        env_file = ".env"

settings = Settings()
