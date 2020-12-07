from typing import Any, Dict, List, Optional

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


class Role(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str


class Author(BaseModel):
    id: str
    name: str
    slug: str
    email: Optional[str]
    profile_image: Optional[str]
    cover_image: Optional[str]
    bio: Optional[str]
    website: Optional[str]
    location: Optional[str]
    twitter: Optional[str]
    status: str
    tour: str
    last_seen: str
    created_at: str
    updated_at: str
    roles: List[Role]
    url: Optional[str]


class Tag(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str]
    visibility: str
    meta_title: Optional[str]
    meta_description: Optional[str]
    created_at: str
    updated_at: str
    og_title: Optional[str]
    og_description: Optional[str]
    twitter_title: Optional[str]
    twitter_description: Optional[str]
    accent_color: Optional[str]
    url: Optional[str]


class PrimaryAuthor(BaseModel):
    id: str
    name: str
    slug: str
    email: Optional[str]
    profile_image: Optional[str]
    cover_image: Optional[str]
    bio: Optional[str]
    website: Optional[str]
    location: Optional[str]
    twitter: Optional[str]
    status: str
    tour: Optional[str]
    last_seen: str
    created_at: str
    updated_at: str
    roles: List[Role]
    url: Optional[str]


class PrimaryTag(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str]
    visibility: str
    meta_title: Optional[str]
    meta_description: Optional[str]
    created_at: str
    updated_at: str
    og_title: Optional[str]
    og_description: Optional[str]
    twitter_title: Optional[str]
    twitter_description: Optional[str]
    accent_color: Optional[str]
    url: Optional[str]


class Current(BaseModel):
    id: str
    uuid: str
    title: Optional[str]
    slug: str
    mobiledoc: Optional[str] = None
    html: Optional[str] = None
    comment_id: str
    plaintext: Optional[str]
    feature_image: Optional[str] = None
    featured: bool
    status: str
    visibility: str
    email_recipient_filter: Optional[str]
    created_at: str
    updated_at: str
    custom_excerpt: Optional[str] = None
    authors: List[Author]
    tags: Optional[List[Tag]] = None
    primary_author: Optional[PrimaryAuthor]
    primary_tag: Optional[PrimaryTag] = None
    url: Optional[str]
    excerpt: Optional[str] = None
    reading_time: int
    send_email_when_published: bool
    og_image: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    twitter_image: Optional[str] = None
    twitter_title: Optional[str] = None
    twitter_description: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class Post(BaseModel):
    current: Current
    previous: Optional[Dict[str, Any]]


class PostUpdate(BaseModel):
    post: Post
