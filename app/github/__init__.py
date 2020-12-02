"""Notify upon Github activity."""
from flask import current_app as api
from flask import make_response, request

from clients import sms
from clients.log import LOGGER


@LOGGER.catch
@api.route("/github/pr", methods=["POST"])
def github_pr():
    """Send SMS notification for all PR activity."""
    payload = request.get_json()
    action = payload.get("action")
    user = payload["sender"].get("login")
    pull_request = payload["pull_request"]
    repo = payload["repository"]
    headers = {"content-type": "text/html; charset=UTF-8"}
    if user in ("toddbirchard", "dependabot-preview[bot]", "renovate[bot]"):
        return make_response(f"Activity from {user} ignored.", 200, headers)
    message = f'PR {action} for repository {repo["name"]}: {pull_request["title"]}` \n\n {pull_request["url"]}'
    LOGGER.info(message)
    sms.send_message(message)
    return make_response(
        f"SMS notification sent for {action} for {user}.", 200, headers
    )


@LOGGER.catch
@api.route("/github/issue", methods=["POST"])
def github_issue():
    """Send SMS notification upon issue creation."""
    payload = request.get_json()
    action = payload.get("action")
    user = payload["sender"].get("login")
    issue = payload["issue"]
    repo = payload["repository"]
    headers = {"content-type": "text/html; charset=UTF-8"}
    if user in ("toddbirchard", "dependabot-preview[bot]", "renovate[bot]"):
        return make_response(f"Activity from {user} ignored.", 200, headers)
    message = f'Issue {action} for repository {repo["name"]}: `{issue["title"]}` \n\n {issue["url"]}'
    LOGGER.info(message)
    sms.send_message(message)
    return make_response(
        f"SMS notification sent for {action} for {user}.", 200, headers
    )