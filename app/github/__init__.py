"""Notify upon Github activity."""
from fastapi import APIRouter, Request

from clients import sms
from clients.log import LOGGER

router = APIRouter(prefix="/github", tags=["github"])


@router.post("/pr")
async def github_pr(request: Request):
    """Send SMS notification for all PR activity."""
    payload = await request.json()
    action = payload.action
    user = payload["sender"].get("login")
    pull_request = payload["pull_request"]
    repo = payload["repository"]
    if user in ("toddbirchard", "dependabot-preview[bot]", "renovate[bot]"):
        return f"Activity from {user} ignored."
    message = f'PR {action} for repository {repo["name"]}: {pull_request["title"]}` \n\n {pull_request["url"]}'
    LOGGER.info(message)
    sms.send_message(message)
    return {f"SMS notification sent for {action} for {user}."}


@router.post("/issue")
async def github_issue(request: Request):
    """Send SMS notification upon issue creation."""
    payload = await request.json()
    action = payload.get("action")
    user = payload["sender"].get("login")
    issue = payload["issue"]
    repo = payload["repository"]
    if user in ("toddbirchard", "dependabot-preview[bot]", "renovate[bot]"):
        return {f"Activity from {user} ignored."}
    message = f'Issue {action} for repository {repo["name"]}: `{issue["title"]}` \n\n {issue["url"]}'
    LOGGER.info(message)
    sms.send_message(message)
    return {f"SMS notification sent for {action} for {user}."}
