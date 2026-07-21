from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.comments import router as comments_router
from app.api.health import router as health_router
from app.api.posts import router as posts_router
from app.api.public import router as public_router

app = FastAPI(title="roselabs-blog")
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(public_router)
app.include_router(comments_router)
