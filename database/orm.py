from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import settings

blog_engine = create_async_engine(
    f"{settings.SQLALCHEMY_DATABASE_URI}/hackers_prod",
    connect_args=settings.SQLALCHEMY_ENGINE_OPTIONS,
    echo=False
)

BlogSession = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=blog_engine,
    expire_on_commit=False,
)

analytics_engine = create_async_engine(
    f"{settings.SQLALCHEMY_DATABASE_URI}/analytics",
    connect_args=settings.SQLALCHEMY_ENGINE_OPTIONS,
    echo=False
)

AnalyticsSession = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=analytics_engine,
    expire_on_commit=False,
)


def get_blog_db():
    async with BlogSession() as session:
        yield session


def get_analytics_db():
    async with AnalyticsSession() as session:
        yield session

