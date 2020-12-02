"""Initialize app."""
from functools import lru_cache

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import analytics, newsletter, posts, accounts, authors
import config


@lru_cache()
def get_settings():
    return config.Settings()


api = FastAPI(
    title="Jamstack API",
    description="API to automate optimizations for JAMStack sites.",
    version="0.1.0",
    debug=True,
    docs_url="/",
    openapi_url="/api.json",
    openapi_tags=[
        {
            "name": "posts",
            "description": "Sanitation and optimization of post data.",
        },
        {
            "name": "accounts",
            "description": "User account signup and actions.",
        },
        {
            "name": "authors",
            "description": "New author management.",
        },
        {
            "name": "newsletter",
            "description": "Ghost newsletter subscription management.",
        },
        {
            "name": "analytics",
            "description": "Fetch site traffic & search query analytics.",
        },
    ],
)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
settings = Depends(get_settings)
api.include_router(analytics.router)
api.include_router(newsletter.router)
api.include_router(posts.router)
api.include_router(accounts.router)
api.include_router(authors.router)
