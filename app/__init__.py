"""Initialize api."""
from ddtrace import patch_all
from ddtrace.contrib.asgi import TraceMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import accounts, analytics, authors, github, images, newsletter, posts
from config import settings
from database.orm import Base, engine

patch_all()
Base.metadata.create_all(bind=engine)


api = FastAPI(
    title="Jamstack API",
    description="API to automate optimizations for JAMStack sites.",
    version="0.1.0",
    debug=True,
    docs_url="/",
    openapi_url="/api.json",
    openapi_tags=settings.API_TAGS,
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(analytics.router)
api.include_router(newsletter.router)
api.include_router(posts.router)
api.include_router(accounts.router)
api.include_router(authors.router)
api.include_router(images.router)
api.include_router(github.router)

if settings.ENVIRONMENT == "production":
    api = TraceMiddleware(api)
