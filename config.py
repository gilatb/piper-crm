import logging
import os

from fastapi.logger import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Piper CRM"
    debug: bool = True
    service_host: str = "0.0.0.0"
    service_port: int = 8000
    log_level: str = "info"

    database_url: str = os.getenv('DATABASE_URL')  # type: ignore
    database_role: str = os.getenv('DATABASE_ROLE')  # type: ignore

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()   # type: ignore


def init_logging():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(settings.log_level.upper())


init_logging()
