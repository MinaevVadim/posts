from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = f"{Path(__file__).parent.parent}/.env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=ENV_FILE,
    )
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: str = 5672


settings = Settings()
