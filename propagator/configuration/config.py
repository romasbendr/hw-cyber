from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    PERIOD_SECONDS: int
    CONSUMER_ENDPOINT: str
    EVENTS_FILE: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env-propagator")


settings = Settings()
