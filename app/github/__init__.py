"""Notify upon Github activity."""
from fastapi import APIRouter, Request

from app.moment import get_current_time
from clients import sms
from clients.log import LOGGER

router = APIRouter(prefix="/github", tags=["github"])


@router.post(
    "/pr",
    summary="Notify upon Github PR creation.",
    description="Send SMS and Discord notifications upon PR creation in HackersAndSlackers Github projects.",
)
async def github_pr(request: Request):
    """
    Send SMS and Discord notifications upon PR creation in HackersAndSlackers Github projects.

    :param request: Incoming Github payload for newly opened PR.
    :type request: Request
    """
    payload = await request.json()
    action = payload.get("action")
    user = payload["sender"].get("login")
    pull_request = payload["pull_request"]
    repo = payload["repository"]
    if user in ("toddbirchard", "dependabot-preview[bot]", "renovate[bot]"):
        return {
            "notification": {
                "time": get_current_time(),
                "status": "ignored",
                "trigger": {
                    "type": "github",
                    "repo": repo["name"],
                    "title": pull_request["title"],
                    "user": user,
                    "action": action,
                },
            }
        }
    message = f'PR {action} for `{repo["name"]}`: \n \
     {pull_request["title"]}  \
     {pull_request["body"]} \
     {pull_request["url"]}'
    sms_message = sms.send_message(message)
    LOGGER.info(f"Github PR {action} for {repo['name']} generated SMS message")
    return {
        "notification": {
            "time": get_current_time(),
            "status": sms_message.status,
            "trigger": {
                "type": "github",
                "repo": repo["name"],
                "title": pull_request["title"],
                "user": user,
                "action": action,
            },
            "sms": {
                "to": sms_message.to,
                "from": sms_message.from_,
                "date_sent": sms_message.date_sent,
                "message": sms_message.body,
            },
        },
    }


@router.post(
    "/issue",
    summary="Notify upon Github Issue creation.",
    description="Send SMS and Discord notifications upon Issue creation in HackersAndSlackers Github projects.",
)
async def github_issue(request: Request) -> dict:
    """
    Send SMS and Discord notifications upon issue creation for HackersAndSlackers Github projects.

    :param request: Incoming Github payload for newly opened issue.
    :type request: Request
    """
    payload = await request.json()
    action = payload.get("action")
    user = payload["sender"].get("login")
    issue = payload["issue"]
    repo = payload["repository"]
    if user in ("toddbirchard", "dependabot-preview[bot]", "renovate[bot]"):
        return {
            "notification": {
                "time": get_current_time(),
                "status": "ignored",
                "trigger": {
                    "type": "github",
                    "repo": repo["name"],
                    "title": issue["title"],
                    "user": user,
                    "action": action,
                },
            }
        }
    message = f'Issue {action} for repository {repo["name"]}: `{issue["title"]}` \n\n {issue["url"]}'
    sms_message = sms.send_message(message)
    LOGGER.info(f"Github issue {action} for {repo['name']} generated SMS message")
    return {
        "notification": {
            "time": get_current_time(),
            "status": sms_message.status,
            "trigger": {
                "type": "github",
                "repo": repo["name"],
                "title": issue["title"],
                "user": user,
                "action": action,
            },
            "sms": {
                "to": sms_message.to,
                "from": sms_message.from_,
                "date_sent": sms_message.date_sent,
                "message": sms_message.body,
            },
        },
    }
