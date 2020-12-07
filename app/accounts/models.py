from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Donation(BaseModel):
    id: int
    email: str
    name: str
    count: int
    message: str
    link: str
    created_at: datetime
    coffee_id: str

    class Config:
        orm_mode = True


class NetlifyUser(BaseModel):
    id: str
    uuid: str
    email: str
    name: Optional[str]
    note: Optional[str] = None
    subscribed: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]
    labels: Optional[List] = None
    avatar_image: Optional[str] = None
    comped: Optional[bool]

    class Config:
        orm_mode = True


class NewUser(BaseModel):
    current: Optional[NetlifyUser]


class UserEvent(BaseModel):
    member: NewUser


class Comment(BaseModel):
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
