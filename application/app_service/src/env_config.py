from pathlib import Path


from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = f"{Path(__file__).parent.parent}/.env"


class AuthJWT(BaseModel):
    private_key_path: Path = Path(__file__).parent / "certs" / "jwt-private.pem"
    public_key_path: Path = Path(__file__).parent / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 45
    refresh_token_expire_days: int = 30


class MediaConf(BaseModel):
    media_host: str = "media"
    media_port: int = 8001


class PostgresConf(BaseModel):
    postgres_name: str = "admin"
    postgres_user: str = "admin"
    postgres_password: str = "admin"
    postgres_port: int = 5432
    postgres_host: str = "postgres"


class RedisConf(BaseModel):
    redis_host: str = "localhost"


class RabbitMQConf(BaseModel):
    rabbitmq_host: str = "localhost"
    rabbitmq_port: str = 5672


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=ENV_FILE,
    )

    auth_jwt: AuthJWT = AuthJWT()
    media: MediaConf = MediaConf()
    postgres: PostgresConf = PostgresConf()
    redis: RedisConf = RedisConf()
    rabbitmq: RabbitMQConf = RabbitMQConf()


settings = Settings()
