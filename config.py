import logging
import os

from dotenv import load_dotenv
from fastapi.logger import logger
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Piper CRM"
    debug: bool = True
    service_host: str = "0.0.0.0"  # nosec[B104]
    service_port: int = 8000  # nosec[B104]
    log_level: str = "info"
    autoreload: bool = True

    database_url: str = os.getenv('DATABASE_URL')  # type: ignore
    database_role: str = os.getenv('DATABASE_ROLE')  # type: ignore


settings = Settings()   # type: ignore


def init_logging():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(settings.log_level.upper())


init_logging()
