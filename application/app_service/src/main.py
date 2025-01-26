from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from routers.posts import router as post_router
from routers.users import router as user_router
from routers.followers import router as follower_router
from routers.comments import router as comment_router

app = FastAPI()

app.include_router(post_router)
app.include_router(user_router)
app.include_router(follower_router)
app.include_router(comment_router)

Instrumentator().instrument(app).expose(app)
