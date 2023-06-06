"""Fetch site traffic & search query analytics."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.analytics.plausible import top_visited_pages_by_timeframe
from database.crud import update_trending_insights
from database.models import AnalyticsResponse, TrendingPostInsight
from database.orm import get_db
from database.schemas import AnalyticsResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get(
    "/weekly/",
    summary="Import site analytics for past 14 days.",
    description="Import weekly site performance analytics from Plausible to SQL database.",
    response_model=AnalyticsResponse,
    status_code=200,
)
async def trending_site_analytics(db: Session = Depends(get_db)):
    """
    Fetch top performing posts from latest 2 weeks.

    :returns: AnalyticsResponse
    """
    trending_posts = top_visited_pages_by_timeframe("14d", limit=100)
    if not trending_posts:
        raise HTTPException(500, "Error while fetching Plausible analytics.")
    trending_posts_inserted = update_trending_insights(trending_posts)
    if not trending_posts_inserted:
        raise HTTPException(500, "Unexpected error while fetching Plausible analytics from REST API.")
    return AnalyticsResponse(
        count=len(trending_posts),
        results=trending_posts,
    )


@router.get(
    "/yearly/",
    summary="Import site analytics for past year.",
    description="Import monthly site performance analytics from Plausible to SQL database.",
    response_model=AnalyticsResponse,
    status_code=200,
)
async def yearly_site_analytics(db: Session = Depends(get_db)):
    """Fetch top searches for past year."""
    yearly_traffic = top_visited_pages_by_timeframe("12mo", limit=5000)
    if not yearly_traffic:
        raise HTTPException(500, "Unexpected error while fetching Plausible analytics from REST API.")
    return {
        "count": len(yearly_traffic),
        "results": yearly_traffic,
    }


'''@router.get(
    "/searches/",
    summary="Import user search queries.",
    description="Store user search queries to a SQL database for analysis and suggestive search.",
    status_code=200,
)
async def save_user_search_queries() -> JSONResponse:
    """
    Save top search analytics for the current week.

    :returns: JSONResponse
    """
    weekly_searches = persist_algolia_searches(settings.ALGOLIA_TABLE_WEEKLY, "7d")
    monthly_searches = persist_algolia_searches(settings.ALGOLIA_TABLE_MONTHLY, "month")
    if weekly_searches is None or monthly_searches is None:
        HTTPException(500, "Unexpected error when saving search query data.")
    LOGGER.success(
        f"Inserted {len(weekly_searches)} rows into `{settings.ALGOLIA_TABLE_WEEKLY}`, \
            {len(monthly_searches)} into `{settings.ALGOLIA_TABLE_MONTHLY}`"
    )
    return JSONResponse(
        {
            "7-Day": {
                "count": len(weekly_searches),
                "rows": weekly_searches,
            },
            "90-Day": {
                "count": len(monthly_searches),
                "rows": monthly_searches,
            },
        }
    )'''
