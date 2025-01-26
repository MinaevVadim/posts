from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = f"{Path(__file__).parent}/.env"


class S3Storage(BaseModel):
    access_key: str = ""
    secret_key: str = ""
    endpoint_url: str = ""
    bucket_name: str = ""


class MediaConf(BaseModel):
    host_name: str = "media"
    host_port: int = 8001


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=ENV_FILE,
    )

    s3storage: S3Storage = S3Storage()
    media: MediaConf = MediaConf()


settings = Settings()
