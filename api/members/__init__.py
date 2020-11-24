"""Ghost member management."""
from flask import current_app as api
from flask import jsonify, make_response, request
from mixpanel import Mixpanel

from api.members.comments import parse_comment
from api.members.subscriptions import new_ghost_subscription
from clients import db, ghost, mailgun
from clients.log import LOGGER


@api.route("/members/signup", methods=["POST"])
def new_ghost_member():
    """Create Ghost member from Netlify identity signup."""
    data = request.get_json()
    response, code = new_ghost_subscription(data)
    return make_response(response, 202)


@LOGGER.catch
@api.route("/members/comment", methods=["POST"])
def new_comment():
    """Save user-generated comment to SQL table, and notify post author."""
    data = request.get_json()
    post = ghost.get_post(data.get("id"))
    comment = parse_comment(data, post)
    if comment["user_role"] is None:
        mailgun.send_comment_notification_email(post, comment)
    existing_comment = db.fetch_records(
        f"SELECT * FROM comments WHERE id = '{data.get('id')}';",
        "hackers_prod",
    )
    if existing_comment is None:
        rows = db.insert_records(
            [comment], table_name="comments", database_name="hackers_prod"
        )
        if bool(rows):
            LOGGER.success(
                f"New comment `{data.get('id')}` saved on post `{data.get('post_slug')}`"
            )
            ghost.rebuild_netlify_site()
            return make_response(comment, 200, {"content-type": "application/json"})
        LOGGER.warning(f"Comment `{data.get('id')}` already exists.")
        return make_response(
            {
                "errors": f"Failed to save duplicate comment `{data.get('id')}`",
                "comment": comment,
            },
            422,
            {"content-type": "application/json"},
        )
    return make_response(
        comment,
        202,
        {"content-type": "application/json"},
    )


@api.route("/members/mixpanel", methods=["POST"])
def subscriber_mixpanel():
    """Create Mixpanel record for newsletter subscriber."""
    mp = Mixpanel(api.config["MIXPANEL_API_TOKEN"])
    data = request.get_json()
    email = data.get("email")
    name = data.get("name")
    if email:
        body = {"$name": name, "$email": email}
        mp.people_set(email, body)
        LOGGER.info(f"Created Mixpanel record for subscriber {name}, ({email}).")
        return make_response(jsonify({"CREATED": body}))
    return make_response(jsonify({"DENIED": data}))


@api.route("/members/donation", methods=["PUT"])
def donation_received():
    """Add donation to historical ledger."""
    donation = request.get_json()
    email = donation.get("email")
    name = donation.get("name")
    link = donation.get("link")
    created_at = donation.get("created_at")
    count = donation.get("count")
    coffee_id = donation.get("coffee_id")
    message = donation.get("message")
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
        database_name="analytics",
    )
    if existing_donation and email:
        db.execute_query(f"DELETE FROM donations WHERE email = {email}")
    db.insert_records(
        [donation_data], table_name="donations", database_name="analytics"
    )
    LOGGER.success(f"Received donation: {donation}")
    return make_response(
        jsonify({"Inserted": donation}), 200, {"content-type": "application/json"}
    )
