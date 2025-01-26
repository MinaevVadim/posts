from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker

from env_config import settings

user = settings.postgres.postgres_user
pwd = settings.postgres.postgres_password
host = settings.postgres.postgres_host
port = settings.postgres.postgres_port
name = settings.postgres.postgres_name

url = f"postgresql+asyncpg://{user}:{pwd}@{host}:{port}/{name}"

engine = create_async_engine(url)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
