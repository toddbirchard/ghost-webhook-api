from typing import Optional, List
from pydantic import BaseModel


class Donation(BaseModel):
    email: str
    name: str
    link: str
    created_at: str
    count: str
    coffee_id: str
    message: str


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


class NewUser(BaseModel):
    current: Optional[NetlifyUser]


class UserEvent(BaseModel):
    member: NewUser


class Comment(BaseModel):
    id: str
    user_name: str
    user_avatar: Optional[str]
    user_id: str
    body: str
    created_at: str
    post_url: str
    post_id: str
    post_slug: str
    user_email: str
    author_name: str
