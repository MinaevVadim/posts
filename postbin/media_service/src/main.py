from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from routers.media import router as media_router

app = FastAPI()

app.include_router(media_router)

Instrumentator().instrument(app).expose(app)
