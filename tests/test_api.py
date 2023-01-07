"""Test API endpoints."""
import pprint

from fastapi.testclient import TestClient
from github import Github
from sqlalchemy.orm import Session

from app import api
from config import settings
from database.schemas import GhostMember, GhostSubscriberRequest, NewDonation

api_test_client = TestClient(api)
pp = pprint.PrettyPrinter(indent=4)


def test_api_docs():
    """API docs health check."""
    response = api_test_client.get("/")
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "text/html; charset=utf-8"


def test_github_pr(github_pr_owner: dict, github_pr_user: dict, gh: Github):
    """
    Create PR in `jamstack-api` repo & send SMS notification.

    :param dict github_pr_owner: GitHub owner of opened PR.
    :param dict github_pr_user: GitHub user updating a PR.
    :param Github gh: GitHub api_test_client.
    """
    owner_response = api_test_client.post("/github/pr/", json=github_pr_owner)
    pr = owner_response.json()["pr"]
    repo = pr["trigger"]["repo"]
    assert owner_response.status_code == 200
    assert owner_response.json()["pr"]["status"] == "ignored"
    assert owner_response.json()["pr"]["trigger"]["type"] == "github"
    assert owner_response.json()["pr"]["trigger"]["repo"] == github_pr_user["pull_request"]["head"]["repo"]["full_name"]

    user_response = api_test_client.post("/github/pr/", json=github_pr_user)
    assert user_response.status_code == 200
    assert user_response.json()["pr"]["trigger"]["type"] == "github"
    assert user_response.json()["pr"]["trigger"]["repo"] == github_pr_user["pull_request"]["head"]["repo"]["full_name"]
    assert user_response.json()["pr"]["status"] == "queued"
    assert user_response.json()["sms"]["phone_sender"] == settings.TWILIO_SENDER_PHONE
    gh.get_repo(repo).get_pull(pr["id"]).edit(state="closed")


def test_github_issue(github_issue_user: dict, gh: Github):
    """
    Trigger issue creation in `jamstack-api` repo & send SMS notification.

    :param dict github_issue_user: GitHub user creating an issue.
    :param Github gh: GitHub api_test_client.
    """
    user_response = api_test_client.post("/github/issue/", json=github_issue_user)
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
    """Run SQL to update Ghost posts' metadata."""
    response = api_test_client.get("/posts/")
    assert response.status_code == 200
    assert response.json().get("inserted") is not None
    assert response.json().get("updated") is not None
    pp.pprint(response.json())


def test_assign_img_alt_attr():
    """Run SQL to update Ghost post image `alt` tags."""
    result = api_test_client.get("/posts/alt/")
    pp.pprint(result.json())


def test_import_site_analytics():
    """Fetch and import site analytics data to SQL."""
    response = api_test_client.get("/analytics/")
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_new_ghost_member():
    """Verify creation of new Ghost newsletter subscriber."""
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
    subscriber = GhostSubscriberRequest(current=member, previous=None)
    response = api_test_client.post("/newsletter/", subscriber)
    assert response.json() is not None


def test_accept_donation(donation: NewDonation, db_session: Session):
    """
    Verify persistence of incoming donation to SQL.

    :param NewDonation donation: Newly submitted donation.
    :param Session db_session: Active database session.
    """
    response = api_test_client.post("/donation/", donation, db_session)
    print(response)
    assert response.status_code == 400


def test_authors_bulk_update_metadata():
    """Verify SQL to update author page metadata."""
    response = api_test_client.get("/authors/")
    assert response.status_code == 200


def test_get_comments():
    """Verify fetching of all Ghost comments."""
    response = api_test_client.get("/account/comments/")
    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()) > 0
    assert response.json()[0]["html"] is not None
