from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    CONSUMER_PORT: int
    STORAGE_TYPE: str
    STORAGE_FILE: str
    DB_URL: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env-consumer")


settings = Settings()
