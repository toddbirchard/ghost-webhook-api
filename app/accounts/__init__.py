"""Ghost member management."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.accounts.comments import parse_comment
from app.accounts.subscriptions import new_ghost_subscription
from clients import db, ghost, mailgun
from .models import UserEvent, Comment, Donation
from .mixpanel import create_mixpanel_record
from clients.log import LOGGER


router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/")
def new_ghost_member(user_event: UserEvent):
    """Create Ghost member from Netlify identity signup."""
    user = user_event.member.current
    response, code = new_ghost_subscription(user)
    mx = create_mixpanel_record(user)
    return {"ghost": response, "mixpanel": mx}


@router.post("/comment")
def new_comment(comment: Comment):
    """Save user-generated comment to SQL table, and notify post author."""
    post = ghost.get_post(comment.post_id)
    if comment.user_email not in ghost.get_authors():
        mailgun.send_comment_notification_email(post, comment.__dict__)
    existing_comment = db.fetch_records(
        f"SELECT * FROM comments WHERE id = '{comment.id}';",
        "hackers_prod",
    )
    if existing_comment is None:
        rows = db.insert_records([comment], "comments", "hackers_prod")
        if bool(rows):
            LOGGER.success(
                f"New comment `{comment.id}` saved on post `{comment.post_slug}`"
            )
            ghost.rebuild_netlify_site()
            return JSONResponse(comment, 200, {"content-type": "application/json"})
        LOGGER.warning(f"Comment `{comment.id}` already exists.")
        return JSONResponse(
            {
                "errors": f"Failed to save duplicate comment `{comment.id}`",
                "comment": comment,
            },
            422,
            {"content-type": "application/json"},
        )
    return JSONResponse(
        comment,
        202,
        {"content-type": "application/json"},
    )


@router.put("/donation")
def donation_received(donation: Donation):
    """Add donation to historical ledger."""
    email = donation.email
    name = donation.name
    link = donation.link
    created_at = donation.created_at
    count = donation.count
    coffee_id = donation.coffee_id
    message = donation.message
    if message:
        message = message.replace("'", "\\'")
    donation_data = {
        "email": email,
        "name": name,
        "link": link,
        "created_at": created_at,
        "count": count,
        "coffee_id": coffee_id,
        "message": message,
    }
    existing_donation = db.fetch_record(
        f"SELECT * FROM donations WHERE email = '{email}';",
        "analytics",
    )
    if existing_donation and email:
        db.execute_query(
            f"DELETE FROM donations WHERE email = '{email}';", "hackers_prod"
        )
    db.insert_records([donation_data], "donations", "analytics")
    LOGGER.success(f"Received donation: {donation}")
    return JSONResponse(
        {"Inserted": donation}, 200, {"content-type": "application/json"}
    )
