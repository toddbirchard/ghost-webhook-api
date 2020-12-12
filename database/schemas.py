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
        schema_extra = {
            "coffee_id": 405127,
            "count": 1,
            "created_at": "2020-12-02",
            "email": "fake@example.com",
            "link": "https://buymeacoffee.com/hackersslackers",
            "name": "Someone",
            "price": "5.00",
        }


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
        schema_extra = {
            "body": "hello",
            "comment_id": "5acfd461583e28622a7833f9",
            "created_at": "2020-12-12T05:26:14.794Z",
            "email": "fake@example.com",
            "post_id": "5dc42cb812c9ce0d63f5bf96",
            "post_slug": "python-virtualenv-virtualenvwrapper",
            "post_url": "https://hackersandslackers.com/python-virtualenv-virtualenvwrapper/",
            "user_avatar": "https://avatars3.githubusercontent.com/u/2747442?v=4",
            "user_email": "toddbirchard@gmail.com",
            "user_id": "8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385",
            "user_name": "Fake Name",
        }


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

    class Config:
        schema_extra = {
            "post": {
                "current": {
                    "id": "5e5cbed04965476b6cd6f16d",
                    "uuid": "242bc890-4537-453b-a85c-690fabf4b6f2",
                    "title": "Lynx Roundup, March 4th 2020",
                    "slug": "lynx-roundup-march-4th-2020",
                    "mobiledoc": '{"version":"0.3.1","atoms":[],"cards":[["bookmark",{"type":"bookmark","url":"https://medium.com/cantors-paradise/dijkstras-shortest-path-algorithm-in-python-d955744c7064","metadata":{"url":"https://medium.com/cantors-paradise/dijkstras-shortest-path-algorithm-in-python-d955744c7064","title":"Dijkstra’s Shortest Path Algorithm in Python","description":"From GPS navigation to network-layer link-state routing, Dijkstra’s Algorithm powers some of the most taken-for-granted modern services. Utilizing some basic data structures, let’s get an…","author":"Micah Shute","publisher":"Cantor’s Paradise","thumbnail":"https://miro.medium.com/max/1200/1*UEBb_0AUZf1QxVOHY71xRA.png","icon":"https://cdn-images-1.medium.com/fit/c/152/152/1*8I-HPL0bfoIzGied-dzOvA.png"}}],["bookmark",{"type":"bookmark","url":"https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace","metadata":{"url":"https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace","title":"Turn Python Scripts into Beautiful ML Tools","description":"In my experience, every nontrivial machine learning project is eventually stitched together with bug-ridden and unmaintainable internal tools. These tools — often a patchwork of Jupyter Notebooks…","author":"Adrien Treuille","publisher":"Towards Data Science","thumbnail":"https://miro.medium.com/freeze/max/640/1*Mbn2SxozueUkGKPW1NJkOw.gif","icon":"https://cdn-images-1.medium.com/fit/c/152/152/1*8I-HPL0bfoIzGied-dzOvA.png"}}],["bookmark",{"type":"bookmark","url":"https://github.com/jyhjinghwang/SegSort","metadata":{"url":"https://github.com/jyhjinghwang/SegSort","title":"jyhjinghwang/SegSort","description":"SegSort: Segmentation by Discriminative Sorting of Segments - jyhjinghwang/SegSort","author":"jyhjinghwang","publisher":"GitHub","thumbnail":"https://avatars3.githubusercontent.com/u/7334548?s=400&v=4","icon":"https://github.githubassets.com/favicon.ico"}}]],"markups":[["a",["href","https://docs.python-guide.org/writing/tests/"]],["a",["href","https://www.bloomberg.com/news/features/2019-09-25/polypropylene-plastic-can-finally-be-recycled"]],["a",["href","https://lectures.quantecon.org/_downloads/pdf/py/Quantitative%20Economics%20with%20Python.pdf"]]],"sections":[[10,0],[10,1],[10,2],[1,"p",[[0,[0],1,"https://docs.python-guide.org/writing/tests/"]]],[1,"p",[[0,[1],1,"https://www.bloomberg.com/news/features/2019-09-25/polypropylene-plastic-can-finally-be-recycled"]]],[1,"p",[[0,[2],1,"https://lectures.quantecon.org/_downloads/pdf/py/Quantitative Economics with Python.pdf"]]]]}',
                    "html": '<figure class="kg-card kg-bookmark-card"><a class="kg-bookmark-container" href="https://medium.com/cantors-paradise/dijkstras-shortest-path-algorithm-in-python-d955744c7064"><div class="kg-bookmark-content"><div class="kg-bookmark-title">Dijkstra’s Shortest Path Algorithm in Python</div><div class="kg-bookmark-description">From GPS navigation to network-layer link-state routing, Dijkstra’s Algorithm powers some of the most taken-for-granted modern services. Utilizing some basic data structures, let’s get an…</div><div class="kg-bookmark-metadata"><img class="kg-bookmark-icon" src="https://cdn-images-1.medium.com/fit/c/152/152/1*8I-HPL0bfoIzGied-dzOvA.png"><span class="kg-bookmark-author">Micah Shute</span><span class="kg-bookmark-publisher">Cantor’s Paradise</span></div></div><div class="kg-bookmark-thumbnail"><img src="https://miro.medium.com/max/1200/1*UEBb_0AUZf1QxVOHY71xRA.png"></div></a></figure><figure class="kg-card kg-bookmark-card"><a class="kg-bookmark-container" href="https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace"><div class="kg-bookmark-content"><div class="kg-bookmark-title">Turn Python Scripts into Beautiful ML Tools</div><div class="kg-bookmark-description">In my experience, every nontrivial machine learning project is eventually stitched together with bug-ridden and unmaintainable internal tools. These tools — often a patchwork of Jupyter Notebooks…</div><div class="kg-bookmark-metadata"><img class="kg-bookmark-icon" src="https://cdn-images-1.medium.com/fit/c/152/152/1*8I-HPL0bfoIzGied-dzOvA.png"><span class="kg-bookmark-author">Adrien Treuille</span><span class="kg-bookmark-publisher">Towards Data Science</span></div></div><div class="kg-bookmark-thumbnail"><img src="https://miro.medium.com/freeze/max/640/1*Mbn2SxozueUkGKPW1NJkOw.gif"></div></a></figure><figure class="kg-card kg-bookmark-card"><a class="kg-bookmark-container" href="https://github.com/jyhjinghwang/SegSort"><div class="kg-bookmark-content"><div class="kg-bookmark-title">jyhjinghwang/SegSort</div><div class="kg-bookmark-description">SegSort: Segmentation by Discriminative Sorting of Segments - jyhjinghwang/SegSort</div><div class="kg-bookmark-metadata"><img class="kg-bookmark-icon" src="https://github.githubassets.com/favicon.ico"><span class="kg-bookmark-author">jyhjinghwang</span><span class="kg-bookmark-publisher">GitHub</span></div></div><div class="kg-bookmark-thumbnail"><img src="https://avatars3.githubusercontent.com/u/7334548?s=400&amp;v=4"></div></a></figure><p><a href="https://docs.python-guide.org/writing/tests/">https://docs.python-guide.org/writing/tests/</a></p><p><a href="https://www.bloomberg.com/news/features/2019-09-25/polypropylene-plastic-can-finally-be-recycled">https://www.bloomberg.com/news/features/2019-09-25/polypropylene-plastic-can-finally-be-recycled</a></p><p><a href="https://lectures.quantecon.org/_downloads/pdf/py/Quantitative%20Economics%20with%20Python.pdf">https://lectures.quantecon.org/_downloads/pdf/py/Quantitative Economics with Python.pdf</a></p>',
                    "comment_id": "5e5cbed04965476b6cd6f16d",
                    "plaintext": "Dijkstra’s Shortest Path Algorithm in PythonFrom GPS navigation to\nnetwork-layer\nlink-state routing, Dijkstra’s Algorithm powers some of the most\ntaken-for-granted modern services. Utilizing some basic data structures, let’s\nget an…Micah ShuteCantor’s Paradise\n[https://medium.com/cantors-paradise/dijkstras-shortest-path-algorithm-in-python-d955744c7064]\nTurn Python Scripts into Beautiful ML ToolsIn my experience, every nontrivial\nmachine learning project is eventually stitched together with bug-ridden and\nunmaintainable internal tools. These tools — often a patchwork of Jupyter\nNotebooks…Adrien TreuilleTowards Data Science\n[https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace]\njyhjinghwang/SegSortSegSort: Segmentation by Discriminative Sorting of Segments\n- jyhjinghwang/SegSortjyhjinghwangGitHub\n[https://github.com/jyhjinghwang/SegSort]\nhttps://docs.python-guide.org/writing/tests/\n\nhttps://www.bloomberg.com/news/features/2019-09-25/polypropylene-plastic-can-finally-be-recycled\n\nhttps://lectures.quantecon.org/_downloads/pdf/py/Quantitative Economics with\nPython.pdf\n[https://lectures.quantecon.org/_downloads/pdf/py/Quantitative%20Economics%20with%20Python.pdf]",
                    "feature_image": "https://hackersandslackers-cdn.storage.googleapis.com/roundup/125.jpg",
                    "featured": False,
                    "status": "published",
                    "visibility": "public",
                    "email_recipient_filter": "none",
                    "created_at": "2020-03-02T08:07:44.000Z",
                    "updated_at": "2020-03-06T03:48:11.000Z",
                    "published_at": "2020-03-04T12:00:00.000Z",
                    "custom_excerpt": "Quantum economics with Python! Turn Python scripts into ML tools!  Dijkstra’s 'shortest path' algorithm in Python!",
                    "authors": [
                        {
                            "id": "5dc42cb612c9ce0d63f5bf39",
                            "name": "Mister Man",
                            "slug": "man",
                            "email": "fake@example.com",
                            "profile_image": "https://hackersandslackers-cdn.storage.googleapis.com/authors/mattavi@2x.jpg",
                            "cover_image": "https://hackersandslackers-cdn.storage.googleapis.com/2020/03/lynxy.jpg",
                            "bio": "Supervillain in somebody's action hero movie. Experienced a radioactive freak accident at a young age which rendered him part-snake and strangely adept at Python.\n\n",
                            "website": "https://github.com/mattalhonte",
                            "location": "Center of the Universe",
                            "twitter": "@MisterMan",
                            "status": "active",
                            "tour": '["getting-started"]',
                            "last_seen": "2020-11-20T05:32:19.000Z",
                            "created_at": "2018-04-16T03:42:48.000Z",
                            "updated_at": "2020-11-20T05:32:19.000Z",
                            "roles": [
                                {
                                    "id": "5dc42c6b4b25bc0d13674448",
                                    "name": "Administrator",
                                    "description": "Administrators",
                                    "created_at": "2019-11-07T14:38:35.000Z",
                                    "updated_at": "2019-11-07T14:38:35.000Z",
                                }
                            ],
                            "url": "https://hackersandslackers.app/author/matt/",
                        }
                    ],
                    "tags": [
                        {
                            "id": "5dc42cb712c9ce0d63f5bf54",
                            "name": "Roundup",
                            "slug": "roundup",
                            "description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                            "visibility": "public",
                            "meta_title": "Data Science News Daily Roundup",
                            "meta_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                            "created_at": "2018-04-16T23:26:05.000Z",
                            "updated_at": "2020-08-04T22:14:59.000Z",
                            "og_title": "Data Science News Daily Roundup",
                            "og_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                            "twitter_title": "Data Science News Daily Roundup",
                            "twitter_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                            "accent_color": "#897ecb",
                            "url": "https://hackersandslackers.app/tag/roundup/",
                        }
                    ],
                    "primary_author": {
                        "id": "5dc42cb612c9ce0d63f5bf39",
                        "name": "Mister Man",
                        "slug": "man",
                        "email": "fake@example.com",
                        "profile_image": "https://hackersandslackers-cdn.storage.googleapis.com/authors/mattavi@2x.jpg",
                        "cover_image": "https://hackersandslackers-cdn.storage.googleapis.com/2020/03/lynxy.jpg",
                        "bio": "Supervillain in somebody's action hero movie. Experienced a radioactive freak accident at a young age which rendered him part-snake and strangely adept at Python.\n\n",
                        "website": "https://github.com/mattalhonte",
                        "location": "Center of the Universe",
                        "twitter": "@MisterMan",
                        "status": "active",
                        "tour": '["getting-started"]',
                        "last_seen": "2020-11-20T05:32:19.000Z",
                        "created_at": "2018-04-16T03:42:48.000Z",
                        "updated_at": "2020-11-20T05:32:19.000Z",
                        "roles": [
                            {
                                "id": "5dc42c6b4b25bc0d13674448",
                                "name": "Administrator",
                                "description": "Administrators",
                                "created_at": "2019-11-07T14:38:35.000Z",
                                "updated_at": "2019-11-07T14:38:35.000Z",
                            }
                        ],
                        "url": "https://hackersandslackers.app/author/matt/",
                    },
                    "primary_tag": {
                        "id": "5dc42cb712c9ce0d63f5bf54",
                        "name": "Roundup",
                        "slug": "roundup",
                        "description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                        "visibility": "public",
                        "meta_title": "Data Science News Daily Roundup",
                        "meta_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                        "created_at": "2018-04-16T23:26:05.000Z",
                        "updated_at": "2020-08-04T22:14:59.000Z",
                        "og_title": "Data Science News Daily Roundup",
                        "og_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                        "twitter_title": "Data Science News Daily Roundup",
                        "twitter_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                        "accent_color": "#897ecb",
                        "url": "https://hackersandslackers.app/tag/roundup/",
                    },
                    "url": "https://hackersandslackers.app/lynx-roundup-march-4th-2020/",
                    "excerpt": "Quantum economics with Python! Turn Python scripts into ML tools!  Dijkstra’s 'shortest path' algorithm in Python!",
                    "reading_time": 2,
                    "send_email_when_published": False,
                    "og_title": "Lynx Roundup, March 4th 2020",
                    "og_description": "Quantum economics with Python! Turn Python scripts into ML tools!  Dijkstra’s 'shortest path' algorithm in Python!",
                    "twitter_title": "Lynx Roundup, March 4th 2020",
                    "twitter_description": "Quantum economics with Python! Turn Python scripts into ML tools!  Dijkstra’s 'shortest path' algorithm in Python!",
                    "meta_title": "Lynx Roundup, March 4th 2020",
                    "meta_description": "Quantum economics with Python! Turn Python scripts into ML tools!  Dijkstra’s 'shortest path' algorithm in Python!",
                },
                "previous": {},
            }
        }


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

    class Config:
        schema_extra = {
            "member": {
                "current": {
                    "id": "5fc703013448cb765efe3f",
                    "uuid": "20f43355a7-4896-461b-adc9-b71da1a188fa",
                    "email": "fake@example.com",
                    "name": "Fake Name",
                    "note": "dw v fbnhntnhaf",
                    "subscribed": True,
                    "created_at": "2020-12-02T02:59:13.642Z",
                    "updated_at": "2020-12-02T02:59:13.642Z",
                    "labels": [],
                    "avatar_image": "https://gravatar.com/avatar/a94833516733d846f03e678a8b4367e9?s=250&d=blank",
                    "comped": True,
                },
                "previous": {},
            }
        }


class SubscriptionWelcomeEmail(BaseModel):
    from_email: str
    to_email: str
    subject: str
    template: str

    class Config:
        schema_extra = {
            "from_email": "fake@example.com",
            "to_email": "recipient@example.com",
            "subject": "Welcome to Hackers & Slackers",
            "template": "This is an email",
        }


class SMS:
    phone_recipient: str
    phone_sender: str
    date_sent: str
    message: str

    class Config:
        schema_extra = {
            "phone_recipient": "5554201738",
            "phone_sender": "5551738420",
            "date_sent": "2020-12-02T02:59:13.642Z",
            "message": "u up?",
        }


class GithubIssue:
    issue: Dict[str, Any]

    class Config:
        schema_extra = {
            "issue": {
                "time": "2020-12-02T02:59:13.642Z",
                "status": "open",
                "trigger": {
                    "type": "github",
                    "repo": "toddbirchard/jamstack-api",
                    "title": "Jamstack API",
                    "user": "fakeuser",
                    "action": "opened",
                },
            },
        }
