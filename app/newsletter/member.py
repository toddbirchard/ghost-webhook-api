"""Parse Ghost member into JSON response."""
from database.schemas import Member


def parse_ghost_member_json(member: Member) -> dict:
    """
    Transform Ghost `member` object to JSON.

    :param Member member: Ghost member subscribed to receive newsletters.

    :returns: dict
    """
    return {
        "id": member.id,
        "email": member.email,
        "avatar": member.avatar_image,
        "note": member.note,
        "labels": member.labels,
        "created_at": member.created_at if member.created_at else None,
        "updated_at": member.updated_at if member.updated_at else None,
    }
