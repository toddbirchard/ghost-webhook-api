from typing import Optional, List
from pydantic import BaseModel


class Member(BaseModel):
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


class Subscriber(BaseModel):
    current: Optional[Member] = None
    previous: Optional[Member] = None


class Subscription(BaseModel):
    member: Subscriber
