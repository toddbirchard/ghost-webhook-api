"""Plausible analytics testing."""
from app.analytics import fetch_top_visited_urls
from app.analytics.plausible import enrich_url_with_post_data


def test_fetch_top_visited_urls():
    urls = fetch_top_visited_urls("month")
    assert urls is not None
    assert len(urls) > 0
    assert urls[0]["url"] is not None
    assert urls[0]["title"] is not None


def test_enrich_url_with_post_data():
    page_result = {"page": "/flask-routes/", "visitors": 869}
    post_dict = enrich_url_with_post_data(page_result)
    assert post_dict["title"] is not None
    assert post_dict["slug"] is not None
    assert post_dict["slug"] == "flask-routes"
    assert post_dict["title"] == "The Art of Routing in Flask"
