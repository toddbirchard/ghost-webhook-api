"""Test Plausible API's integration to associate views per page"""

from app.analytics.plausible import enrich_url_with_post_data, fetch_top_visited_pages


def test_fetch_top_visited_urls():
    """Test fetching top visited URLs in current month."""
    urls = fetch_top_visited_pages("30d")
    assert urls is not None
    assert len(urls) > 0
    assert urls[0]["page"] is not None
    assert urls[0]["visitors"] is not None
    assert urls[0]["visitors"] > 0


def test_enrich_url_with_post_data():
    """Test enriching Plausible URL with Ghost post data."""
    page_result = {
        "page": "/flask-routes/",
        "pageviews": 2932,
        "visitors": 869,
        "visit_duration": 33,
        "bounce_rate": 10,
    }
    post_dict = enrich_url_with_post_data(page_result)
    assert post_dict["title"] is not None
    assert post_dict["slug"] is not None
    assert post_dict["slug"] == "flask-routes"
    assert post_dict["title"] == "The Art of Routing in Flask"
