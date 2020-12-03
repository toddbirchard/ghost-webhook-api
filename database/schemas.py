from typing import Optional

from pydantic import BaseModel


class NewDonation(BaseModel):
    email: str
    name: str
    count: int
    message: str
    link: str
    created_at: str
    coffee_id: int

    class Config:
        orm_mode = True


class NewComment(BaseModel):
    comment_id: str
    post_id: str
    post_slug: str
    user_id: str
    user_name: str
    user_avatar: Optional[str]
    user_email: str
    body: str
    created_at: str
    author_name: str

    class Config:
        orm_mode = True
