"""Integration tests for API client."""

import pprint

from fastapi.testclient import TestClient
from github import Github

from app import create_app
from config import settings

# from database.schemas import GhostMember, GhostSubscriber, NewDonation

client = TestClient(create_app())
pp = pprint.PrettyPrinter(indent=4)


def test_api_docs():
    """API docs health check."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "text/html; charset=utf-8"


def test_github_pr(github_pr_owner: dict, github_pr_user: dict, gh: Github):
    """
    Create PR in `blog-webhook-api` repo & send SMS notification.

    :param dict github_pr_owner: Github PR event payload for owner.
    :param dict github_pr_user: Github PR event payload for user.
    :param Github gh: Github API client.
    """
    owner_response = client.post("/github/pr/", json=github_pr_owner)
    pr = owner_response.json()["pr"]
    repo = pr["trigger"]["repo"]
    assert owner_response.status_code == 200
    assert owner_response.json()["pr"]["status"] == "ignored"
    assert owner_response.json()["pr"]["trigger"]["type"] == "github"
    assert owner_response.json()["pr"]["trigger"]["repo"] == github_pr_user["pull_request"]["head"]["repo"]["full_name"]

    user_response = client.post("/github/pr/", json=github_pr_user)
    assert user_response.status_code == 200
    assert user_response.json()["pr"]["trigger"]["type"] == "github"
    assert user_response.json()["pr"]["trigger"]["repo"] == github_pr_user["pull_request"]["head"]["repo"]["full_name"]
    assert user_response.json()["pr"]["status"] == "queued"
    assert user_response.json()["sms"]["phone_sender"] == settings.TWILIO_SENDER_PHONE
    gh.get_repo(repo).get_pull(pr["id"]).edit(state="closed")


def test_github_issue(github_issue_user: dict, gh: Github):
    """
    Create issue in `blog-webhook-api` repo & send SMS notification.

    :param dict github_issue_user: Github issue event payload for user.
    :param Github gh: Github API client.
    """
    user_response = client.post("/github/issue/", json=github_issue_user)
    assert user_response.status_code == 200
    issue = user_response.json()["issue"]
    repo = issue["trigger"]["repo"]
    assert issue["status"] == "queued"
    assert issue["trigger"]["type"] == "github"
    assert issue["trigger"]["repo"] == github_issue_user["repository"]["full_name"]
    assert issue["trigger"]["title"] == github_issue_user["issue"]["title"]
    assert user_response.json()["sms"]["phone_sender"] == settings.TWILIO_SENDER_PHONE
    gh_issues = gh.get_repo(repo).get_issues(state="open")
    for gh_issue in gh_issues:
        if gh_issue.title == issue["trigger"]["title"]:
            gh_issue.edit(state="closed")


def test_batch_update_metadata():
    """Test updating metadata for all posts."""
    response = client.get("/posts/")
    assert response.status_code == 200
    # TODO: Add `update` assertions, or remove this test.


def assign_img_alt_attr():
    """Assign `alt` attribute to all images in posts."""
    result = client.get("/posts/alt/")
    pp.pprint(result.json())


def test_import_site_analytics():
    """Fetch site analytics."""
    response = client.get("/analytics/")
    assert response.status_code == 200
    assert type(response.json()) == dict


"""def test_new_ghost_member():
    member = GhostMember(
        id="dfdsgf",
        uuid="dsfdf-dsfdsfsfdsf-sdfdsfdsfsafd",
        name="Example Name",
        note="This is a test note about a Ghost member.",
        subscribed=True,
        email="fakeemail@example.com",
        avatar_image="https://gravatar.com/avatar/a94833516733d846f03e678a8b4367e9?s=250&d=blank",
        labels=["VIP"],
        comped=False,
    )
    subscriber = GhostSubscriber(current=member, previous=None)
    response = client.post("/newsletter/", subscriber)
    assert response.json() is not None


def test_accept_donation(donation: NewDonation):
    response = client.post("/donation/", donation)
    assert response.status_code == 400"""


def test_authors_bulk_update_metadata():
    """Fetch all author info."""
    response = client.get("/authors/")
    assert response.status_code >= 200
