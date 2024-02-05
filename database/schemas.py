"""FastAPI Pydantic Schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class NewDonation(BaseModel):
    """`BuyMeACoffee` donation."""

    # fmt: off
    name: str = Field(None, example="Fake Todd")
    email: str = Field(None, example="fake@example.com")
    count: int = Field(None, example=5)
    message: Optional[str] = Field(None, example="Great tutorials but this is a test message.")
    link: str = Field(None, example="https://buymeacoffee.com/hackersslackers/c/fake")
    coffee_id: int = Field(None, example=3453543)
    # fmt: on

    class Config:
        json_schema_extra = {
            "name": "Fake Todd",
            "email": "fake@example.com",
            "count": 1,
            "message": "Great tutorials but this is a test message.",
            "link": "https://buymeacoffee.com/hackersslackers",
            "coffee_id": 405127,
        }


class NewComment(BaseModel):
    """User comment on a post."""

    # fmt: off
    post_id: str = Field(None, example="61304d8374047afda1c2168b")
    post_slug: str = Field(None, example="python-virtualenv-virtualenvwrapper")
    user_id: str = Field(None, example="677f9417-16ab-4d8e-9bed-1130da250c88")
    user_name: Optional[str] = Field(None, example="Todd Birchard")
    user_avatar: Optional[str] = Field(None, example="https://hackersandslackers-cdn.storage.googleapis.com/2021/09/avimoji.jpg")
    user_email: Optional[str] = Field(None, example="todd@hackersandslackers.com")
    author_name: Optional[str] = Field(None, example="Todd Birchard")
    author_id: str = Field(None, example="1")
    body: Optional[str] = Field(None, example="These tutorials are awesome! 10/10")
    # fmt: on

    class Config:
        json_schema_extra = {
            "post_id": "61304d8374047afda1c2168b",
            "post_slug": "python-virtualenv-virtualenvwrapper",
            "user_avatar": "https://hackersandslackers-cdn.storage.googleapis.com/2021/09/avimoji.jpg",
            "user_email": "todd@fakeemail.com",
            "user_id": "677f9417-16ab-4d8e-9bed-1130da250c88",
            "user_name": "Todd Birchard",
            "author_name": "Todd Birchard",
            "author_id": "1",
            "body": "These tutorials are awesome! 10/10",
        }


class UpvoteComment(BaseModel):
    """User upvote on a comment."""

    comment_id: int = Field(None, example=1)
    user_id: str = Field(None, example="8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385")
    vote: bool = Field(None, example=True)


class Role(BaseModel):
    """User role."""

    id: str = Field(None, example="5dc42c6b4b25bc0d13674448")
    name: str = Field(None, example="Administrator")
    description: str = Field(None, example="Administrators")
    created_at: datetime = Field(None, example=datetime.now())
    created_by: str = Field(None, example=1)
    updated_at: datetime = Field(None, example=1)
    updated_by: str = Field(None, example=datetime.now())


class Author(BaseModel):
    """Author profile."""

    # fmt: off
    id: str = Field(None, example=1)
    name: str = Field(None, example="Todd Birchard")
    slug: str = Field(None, example="todd")
    email: Optional[str] = Field(None, example="fake@example.com")
    profile_image: Optional[str] = Field(None, example="https://cdn.hackersandslackers.com/authors/todd@2x.jpg")
    cover_image: Optional[str] = Field(None, example="https://cdn.hackersandslackers.com/2020/03/fantasticmrfox.jpg")
    bio: Optional[str] = Field(None, example="Engineer with an ongoing identity crisis. Breaks everything before learning best practices. Completely normal and emotionally stable.")
    website: Optional[str] = Field(None, example="https://toddbirchard.com")
    location: Optional[str] = Field(None, example="New York City")
    twitter: Optional[str] = Field(None, example="@ToddRBirchard")
    status: str = Field(None, example="active")
    tour: str = Field(None, example='["upload-a-theme","getting-started"]')
    last_seen: str = Field(None, example="2020-12-20 10:54:20")
    created_at: datetime = Field(None, example="2019-11-07 14:38:35")
    updated_at: datetime = Field(None, example="2020-12-20 10:54:20")
    roles: List[Role]
    url: Optional[str] = Field(None, example="fake@example.com")
    accessibility: str = Field(None, example='{"nightShift":true,"views":[{"name":"WIP","route":"posts","color":"green","filter":{"type":"draft","author":"todd"}},{"name":"Series: Lynx Roundup","route":"posts","color":"pink","filter":{"tag":"roundup"}},{"name":"Series: Building Flask Apps","route":"posts","color":"blue","filter":{"tag":"building-flask-apps","author":"todd"}},{"name":"Series: Pandas","route":"posts","color":"purple","filter":{"tag":"data-analysis-pandas"}},{"name":"Series: Code Snippet Corner","route":"posts","color":"teal","filter":{"tag":"code-snippet-corner"}},{"name":"Todds Posts","route":"posts","color":"midgrey","filter":{"author":"todd"}}],"navigation":{"expanded":{"posts":false}},"whatsNew":{"lastSeenDate":"2021-04-05T16:01:11.000+00:00"}}')
    # fmt: on


class Tag(BaseModel):
    """Post tag."""

    # fmt: off
    id: str = Field(None, example="5dc42cb712c9ce0d63f5bf4f")
    name: str = Field(None, example="Python")
    slug: str = Field(None, example="python")
    description: Optional[str] = Field(None, example="Let us feed your endless Python addiction!")
    feature_image: Optional[str] = Field(None, example="https://cdn.hackersandslackers.com/2020/05/python.png")
    visibility: str = Field(None, example="public")
    meta_title: Optional[str] = Field(None, example="Python Tricks, Hacks, and Snippets")
    meta_description: Optional[str] = Field(None, example="Let us feed your endless Python addiction!")
    created_at: datetime = Field(None, example="2017-11-17 20:44:09")
    updated_at: datetime = Field(None, example="2020-08-03 05:21:42")
    og_title: Optional[str] = Field(None, example="Python Tricks, Hacks, and Snippets")
    og_description: Optional[str] = Field(None, example="Let us feed your endless Python addiction!")
    og_image: Optional[str] = Field(None, example="https://cdn.hackersandslackers.com/2020/05/python.png")
    twitter_title: Optional[str] = Field(None, example="Python Tricks, Hacks, and Snippets")
    twitter_description: Optional[str] = Field(None, example="Let us feed your endless Python addiction!")
    twitter_image: Optional[str] = Field(None, example="https://cdn.hackersandslackers.com/2020/05/python.png")
    accent_color: Optional[str] = Field(None, example="#4B8BBE")
    canonical_url: Optional[str] = None
    # fmt: on


class TagUpdate(BaseModel):
    """Incoming tag update request."""

    current: Tag
    previous: Optional[Tag]


class BasePost(BaseModel):
    """Ghost post."""

    # fmt: off
    id: str = Field(None, example="5dc42cb812c9ce0d63f5bf8e")
    uuid: str = Field(None, example="84d9b616-db30-44f3-9ef3-cfc035ae71f9")
    title: str = Field(None, example="Welcome to Hackers and Slackers")
    slug: str = Field(None, example="welcome-to-hackers-and-slackers")
    mobiledoc: str = Field(None, example='{"version":"0.3.1","atoms":[],"cards":[],"markups":[["a",["href","http://hackersandslackers.com"]]],"sections":[[1,"p",[[0,[],0,"Welcome to the Hackers and Slackers blog, the official counterpart to "],[0,[0],1,"hackersandslackers.com"],[0,[],0,"."]]],[1,"p",[[0,[],0,"H+S is a tightly knit community of of people who code dope shit as a means to an end. While we may not all be developers per se, we like to blow stuff up and make an impact. If we get to pick up a few programming languages in the process, so be it."]]],[1,"p",[[0,[],0,"While we keep most of our knowledge tucked into our confluence instance, this blog is intended to be the public facing fruits of our labor. When we manage to stumble upon making things that are actually useful, this will be our medium for communicating that."]]],[1,"p",[[0,[],0,"If you\'re somebody who likes to learn and be casually badass, maybe you should join us."]]]]}')
    html: Optional[str] = Field(None, example="<!DOCTYPE html><html><head></head><body></body></html>")
    comment_id: str = Field(None, example="5a0f4699e38d612cc8261306")
    plaintext: Optional[str] = Field(None, example="5dc42cb712c9ce0d63f5bf4f")
    feature_image: Optional[str] = Field(None, example="https://cdn.hackersandslackers.com/2017/11/welcome.jpg",)
    featured: bool = Field(None, example=False)
    status: str = Field(None, example="published")
    visibility: str = Field(None, example="public")
    email_subject: Optional[str] = Field(None, example="My Newsletter")
    email_recipient_filter: Optional[str] = Field(None, example=None)
    created_at: datetime = Field(None, example="2017-11-17T20:29:13.000Z")
    updated_at: datetime = Field(None, example="2019-10-26T06:52:53.000Z")
    published_at: str = Field(None, example="2017-11-13T20:37:00.000Z")
    custom_excerpt: Optional[str] = Field(None, example="Technology for badasses.")
    authors: List[Author] = Field(None, example=[Author.schema()])
    tags: Optional[List[Tag]] = Field(None, example=[Tag.schema()])
    primary_author: Author = Field(None, example=Author.schema())
    primary_tag: Optional[Tag] = Field(None, example=Tag.schema().get("example"))
    url: Optional[str] = Field(None, example="https://hackersandslackers.com/welcome-to-hackers-and-slackers/")
    excerpt: Optional[str] = Field(None, example="Technology for badasses.")
    reading_time: int = Field(None, example=1)
    send_email_when_published: bool = Field(None, example=False)
    og_image: Optional[str] = Field(None, example="https://cdn.hackersandslackers.com/2017/11/welcome.jpg")
    og_title: Optional[str] = Field(None, example="Welcome to Hackers and Slackers")
    og_description: Optional[str] = Field(None, example="Technology for badasses")
    twitter_image: Optional[str] = Field(None, example="https://cdn.hackersandslackers.com/2017/11/welcome.jpg")
    twitter_title: Optional[str] = Field(None, example="Welcome to Hackers and Slackers")
    twitter_description: Optional[str] = Field(None, example="Technology for badasses")
    meta_title: Optional[str] = Field(None, example="Welcome to Hackers and Slackers")
    meta_description: Optional[str] = Field(None, example="Technology for badasses")
    canonical_url: Optional[str] = Field(None, example="https://hackersandslackers.com/post")
    frontmatter: Optional[str] = Field(None)
    custom_template: Optional[str] = Field(None, example="custom-authors")
    type: str = Field(None, example="Post")
    # fmt: on


class Post(BaseModel):
    """Incoming post update request."""

    current: BasePost
    previous: Optional[BasePost]


class FetchedPost(BaseModel):
    """List of posts fetched from Ghost API."""

    posts: List[BasePost]


class PostUpdate(BaseModel):
    """Incoming post update request."""

    post: Post

    class Config:
        # fmt: off
        json_schema_extra = {
            "current": {
                "id": "61304d8374047afda1c218ff",
                "uuid": "242bc890-4537-453b-a85c-690fabf4b6f2",
                "title": "A Brief History of Pandas",
                "slug": "a-brief-history-of-pandas",
                "mobiledoc": '{"version":"0.3.1","atoms":[["soft-return","",{}],["soft-return","",{}],["soft-return","",{}]],"cards":[["image",{"src":"https://cdn.hackersandslackers.com/2020/02/1024px-Castle_Bravo_Blast.jpg","caption":"Breathe in that whiff of the apocalypse","cardWidth":"","alt":"Breathe in that whiff of the apocalypse"}],["image",{"src":"https://cdn.hackersandslackers.com/2020/02/fear-and-loathing-with-apl-oredev-8-638.jpg","caption":"from here: <a href=\"https://www.slideshare.net/theburningmonk/fear-and-loathing-with-apl-oredev\">https://www.slideshare.net/theburningmonk/fear-and-loathing-with-apl-oredev</a>","alt":"from here: <a href=\"https://www.slideshare.net/theburningmonk/fear-and-loathing-with-apl-oredev\">https://www.slideshare.net/theburningmonk/fear-and-loathing-with-apl-oredev</a>"}]],"markups":[["a",["href","https://en.wikipedia.org/wiki/Fortran#Code_examples"]],["a",["href","https://blog.nuclearsecrecy.com/2013/06/21/castle-bravo-revisited/"]],["a",["href","https://ourcodingclub.github.io/2018/07/30/fortran-intro.html"]],["a",["href","https://www.whoishostingthis.com/resources/apl/"]]],"sections":[[1,"p",[[0,[],0,"Pandas 1.0 came out recently.  To celebrate, here\'s a little tour of what brought us here."]]],[1,"p",[[0,[],0,"There are a lot of places where this story could start, but let\'s start in 1954.  1954 had two events that are pretty important to the birth of Pandas."]]],[1,"h2",[[0,[],0,"Castle Bravo"]]],[10,0],[1,"p",[[0,[],0,"On March 1st, 1954, the US tested a high-yield thermonuclear bomb on Bikini Atoll.  Lithium deuteride (LiD) was the fuel.  Natural lithium includes two different isotopes - Lithium 6 and Lithium 7.  LiD 6 was understood to be Good H-Bomb Fuel, and LiD 7 was used as a moderating substance in the reaction, on the assumption that it was totally inert.  Turns out that this assumption was extremely wrong - the substance that was supposed to moderate the reaction wound up turning into fuel.  What was supposed to be a 6 megaton blast turned out to be a 15 megaton blast."]]],[1,"p",[[0,[],0,"The consequences of this test are far-reaching, both in time and space.  The crew of a Japanese fishing boat suffered acute radiation poisoning, and many people in the Marshall Islands suffered long term harm from fallout.  It lead to an understanding of what fallout actually was, and that you weren\'t safe from a nuclear blast just from being outside of it - it affected people hundreds of miles away.  Castle Bravo also echoes across culture - it helped inspire Godzilla, and it\'s why Spongebob & friends live in \"Bikini Bottom\" (a reference to Bikini Atoll).  Perhaps most saliently, and most relevant to our story, it was a large motivator behind the 1963 Limited Test Ban Treaty, which ended nuclear testing in the atmosphere, underwater, and in space (though there could still be underground tests).  Castle Bravo made it clear just how dangerous these experiments could be, how widespread the damage could be, and that it was basically impossible to guarantee a lack of major mistakes.  "]]],[1,"p",[[0,[],0,"Naturally, this meant a major investment in computer technology to simulate nuclear blasts instead of relying so much on tests.  This technology was already in its infancy, but the mandate for simulating nukes would drive scientific computing until the present day.  This drive for computers and software is ultimately where Silicon Valley comes from.  The Department of Defense and Department of Energy\'s hunger for computers, no matter the cost, lead them to buy up every batch of semiconductors until they were cheap enough to be cost-effective for a more general market."]]],[1,"h2",[[0,[],0,"Fortran"]]],[1,"blockquote",[[0,[],0,"“Much of my work has come from being lazy.  I didn\'t like writing programs, and so, when I was working on the IBM 701, writing programs for computing missile trajectories, I started work on a programming system to make it easier to write programs.” "],[1,[],0,0],[0,[],0,"- John W. Backus"]]],[1,"p",[[0,[],0,"That thought process should seem pretty familiar to any Pandas user - it is essentially what\'s motivated Pandas, R, SQL, and basically any other framework that tries to let you focus on declarative programming for math & data manipulation.  Fortran (a portmanteau on \"Formula Translation\") is a tool for writing scientific programs - it may look verbose compared to equivalent Python code, but it\'s certainly a lot more expressive than Assembly.  You can probably follow the code "],[0,[0],1,"here"],[0,[],0,", which wouldn\'t necessarily be the case with a bunch of Op Codes.  It also has the distinction of being the oldest programming language still in use.  It was developed in 1950, but its first program was run in 1954."]]],[1,"p",[[0,[],0,"Fortran is more than just a spiritual antecedent to scientific computing.  Fortran packages for doing matrix operations, such as BLAS and LAPACK, are \"under the hood\" of Pandas.  The one on your computer isn\'t necessarily written in Fortran - the default is a C translation.  But it\'s an option, where the C one came from, and generally what you want if you really need performance."]]],[1,"p",[[0,[],0,"Note that BLAS, LAPACK, and much of the rest of the scientific Fortran ecosystem remain products of the military-industrial complex.  Or, at least, the ones available open-source.  Organizations like The Department of Energy, DARPA, and the NSF (which has a defense mandate) provide the funding and work hours to keep these packages with fresh updates all the way until today.  And this is part of why it\'s still used - it\'s hard to beat those decades of optimizations."]]],[1,"p",[[0,[],0,"Fortran is only half of our story, however.  Pandas isn\'t just about the fast operations - it\'s also about the syntax."]]],[1,"h2",[[0,[],0,"APL"]]],[10,1],[1,"p",[[0,[],0,"Okay, Fortran is a step up from assembly, but it\'s not really what NumPy or Pandas code looks like.  For that, we need array-based languages with nice vectorized syntax.  There were a few of these kicking around in the 60s and 70s as an example of Convergent Evolution (including S, the predecessor to R) - but I\'m going to talk about APL because it\'s the weirdest, most theoretically-grounded, and I\'m pretty sure Wes McKinney has gone on-record saying it was an inspiration for Pandas."]]],[1,"p",[[0,[],0,"There\'s a saying that there are two types of programming languages - those that start \"from the computer upwards\", and those that start \"from mathematics downward\".  Fortran, for all its relative user-friendliness, still makes you think about things like pre-allocating memory.  APL came from a mathematician named  Kenneth E. Iverson, who came up with a notation for manipulating arrays.  Eventually they wrote up an implementation in Fortran, and it became a for-real programming language."]]],[1,"p",[[0,[],0,"APL was terse, expressive, and made matrix operations a first-class citizen.  Sure, you had to learn a bunch of weird symbols, will need a custom keyboard, and have to internalize a syntax that includes a concept of \"adverbs\".  But, if all you were doing was manipulating data, then that wasn\'t so bad - it certainly matched the thought process more cleanly than repeated assignment statements or explicitly writing loops.  If you like the Tidyverse, method-chaining in Pandas, or even UNIX-style piping, you like this programming paradigm.  It\'s also closer to mathematical notation, which is nice if you\'re wired a certain way and/or have that background."]]],[1,"p",[[0,[],0,"APL was huge, particularly in finance.  Wrapping your mind around imperative code is weird if your training was in mathematical modeling - APL let bankers focus on their models.  And this is still the case - today APL itself is a novelty for the most part, but it survives in the form of J, Q, and most importantly kdb, mostly used in finance.  And of course, Pandas itself was developed while McKinney was working at the hedge fund 2Sigma."]]],[1,"h2",[[0,[],0,"Conclusion"]]],[1,"p",[[0,[],0,"Man, the world\'s weird, right?"]]],[1,"h2",[[0,[],0,"Background Links"]]],[1,"p",[[0,[1],1,"https://blog.nuclearsecrecy.com/2013/06/21/castle-bravo-revisited/"],[1,[],0,1],[0,[2],1,"https://ourcodingclub.github.io/2018/07/30/fortran-intro.html"],[1,[],0,2],[0,[3],1,"https://www.whoishostingthis.com/resources/apl/"]]]],"ghostVersion":"3.0"}',
                "html": '<p>Pandas 1.0 came out recently.  To celebrate, here\'s a little tour of what brought us here.</p><p>There are a lot of places where this story could start, but let\'s start in 1954.  1954 had two events that are pretty important to the birth of Pandas.</p><h2 id="castle-bravo">Castle Bravo</h2><figure class="kg-card kg-image-card kg-card-hascaption"><img src="https://cdn.hackersandslackers.com/2020/02/1024px-Castle_Bravo_Blast.jpg" class="kg-image" alt="Breathe in that whiff of the apocalypse" loading="lazy"><figcaption>Breathe in that whiff of the apocalypse</figcaption></figure><p>On March 1st, 1954, the US tested a high-yield thermonuclear bomb on Bikini Atoll.  Lithium deuteride (LiD) was the fuel.  Natural lithium includes two different isotopes - Lithium 6 and Lithium 7.  LiD 6 was understood to be Good H-Bomb Fuel, and LiD 7 was used as a moderating substance in the reaction, on the assumption that it was totally inert.  Turns out that this assumption was extremely wrong - the substance that was supposed to moderate the reaction wound up turning into fuel.  What was supposed to be a 6 megaton blast turned out to be a 15 megaton blast.</p><p>The consequences of this test are far-reaching, both in time and space.  The crew of a Japanese fishing boat suffered acute radiation poisoning, and many people in the Marshall Islands suffered long term harm from fallout.  It lead to an understanding of what fallout actually was, and that you weren\'t safe from a nuclear blast just from being outside of it - it affected people hundreds of miles away.  Castle Bravo also echoes across culture - it helped inspire Godzilla, and it\'s why Spongebob &amp; friends live in "Bikini Bottom" (a reference to Bikini Atoll).  Perhaps most saliently, and most relevant to our story, it was a large motivator behind the 1963 Limited Test Ban Treaty, which ended nuclear testing in the atmosphere, underwater, and in space (though there could still be underground tests).  Castle Bravo made it clear just how dangerous these experiments could be, how widespread the damage could be, and that it was basically impossible to guarantee a lack of major mistakes.  </p><p>Naturally, this meant a major investment in computer technology to simulate nuclear blasts instead of relying so much on tests.  This technology was already in its infancy, but the mandate for simulating nukes would drive scientific computing until the present day.  This drive for computers and software is ultimately where Silicon Valley comes from.  The Department of Defense and Department of Energy\'s hunger for computers, no matter the cost, lead them to buy up every batch of semiconductors until they were cheap enough to be cost-effective for a more general market.</p><h2 id="fortran">Fortran</h2><blockquote>“Much of my work has come from being lazy.  I didn\'t like writing programs, and so, when I was working on the IBM 701, writing programs for computing missile trajectories, I started work on a programming system to make it easier to write programs.” <br>- John W. Backus</blockquote><p>That thought process should seem pretty familiar to any Pandas user - it is essentially what\'s motivated Pandas, R, SQL, and basically any other framework that tries to let you focus on declarative programming for math &amp; data manipulation.  Fortran (a portmanteau on "Formula Translation") is a tool for writing scientific programs - it may look verbose compared to equivalent Python code, but it\'s certainly a lot more expressive than Assembly.  You can probably follow the code <a href="https://en.wikipedia.org/wiki/Fortran#Code_examples">here</a>, which wouldn\'t necessarily be the case with a bunch of Op Codes.  It also has the distinction of being the oldest programming language still in use.  It was developed in 1950, but its first program was run in 1954.</p><p>Fortran is more than just a spiritual antecedent to scientific computing.  Fortran packages for doing matrix operations, such as BLAS and LAPACK, are "under the hood" of Pandas.  The one on your computer isn\'t necessarily written in Fortran - the default is a C translation.  But it\'s an option, where the C one came from, and generally what you want if you really need performance.</p><p>Note that BLAS, LAPACK, and much of the rest of the scientific Fortran ecosystem remain products of the military-industrial complex.  Or, at least, the ones available open-source.  Organizations like The Department of Energy, DARPA, and the NSF (which has a defense mandate) provide the funding and work hours to keep these packages with fresh updates all the way until today.  And this is part of why it\'s still used - it\'s hard to beat those decades of optimizations.</p><p>Fortran is only half of our story, however.  Pandas isn\'t just about the fast operations - it\'s also about the syntax.</p><h2 id="apl">APL</h2><figure class="kg-card kg-image-card kg-card-hascaption"><img src="https://cdn.hackersandslackers.com/2020/02/fear-and-loathing-with-apl-oredev-8-638.jpg" class="kg-image" alt="from here: <a href=&quot;https://www.slideshare.net/theburningmonk/fear-and-loathing-with-apl-oredev&quot;>https://www.slideshare.net/theburningmonk/fear-and-loathing-with-apl-oredev</a>" loading="lazy"><figcaption>from here: <a href="https://www.slideshare.net/theburningmonk/fear-and-loathing-with-apl-oredev">https://www.slideshare.net/theburningmonk/fear-and-loathing-with-apl-oredev</a></figcaption></figure><p>Okay, Fortran is a step up from assembly, but it\'s not really what NumPy or Pandas code looks like.  For that, we need array-based languages with nice vectorized syntax.  There were a few of these kicking around in the 60s and 70s as an example of Convergent Evolution (including S, the predecessor to R) - but I\'m going to talk about APL because it\'s the weirdest, most theoretically-grounded, and I\'m pretty sure Wes McKinney has gone on-record saying it was an inspiration for Pandas.</p><p>There\'s a saying that there are two types of programming languages - those that start "from the computer upwards", and those that start "from mathematics downward".  Fortran, for all its relative user-friendliness, still makes you think about things like pre-allocating memory.  APL came from a mathematician named  Kenneth E. Iverson, who came up with a notation for manipulating arrays.  Eventually they wrote up an implementation in Fortran, and it became a for-real programming language.</p><p>APL was terse, expressive, and made matrix operations a first-class citizen.  Sure, you had to learn a bunch of weird symbols, will need a custom keyboard, and have to internalize a syntax that includes a concept of "adverbs".  But, if all you were doing was manipulating data, then that wasn\'t so bad - it certainly matched the thought process more cleanly than repeated assignment statements or explicitly writing loops.  If you like the Tidyverse, method-chaining in Pandas, or even UNIX-style piping, you like this programming paradigm.  It\'s also closer to mathematical notation, which is nice if you\'re wired a certain way and/or have that background.</p><p>APL was huge, particularly in finance.  Wrapping your mind around imperative code is weird if your training was in mathematical modeling - APL let bankers focus on their models.  And this is still the case - today APL itself is a novelty for the most part, but it survives in the form of J, Q, and most importantly kdb, mostly used in finance.  And of course, Pandas itself was developed while McKinney was working at the hedge fund 2Sigma.</p><h2 id="conclusion">Conclusion</h2><p>Man, the world\'s weird, right?</p><h2 id="background-links">Background Links</h2><p><a href="https://blog.nuclearsecrecy.com/2013/06/21/castle-bravo-revisited/">https://blog.nuclearsecrecy.com/2013/06/21/castle-bravo-revisited/</a><br><a href="https://ourcodingclub.github.io/2018/07/30/fortran-intro.html">https://ourcodingclub.github.io/2018/07/30/fortran-intro.html</a><br><a href="https://www.whoishostingthis.com/resources/apl/">https://www.whoishostingthis.com/resources/apl/</a></p>',
                "comment_id": "5e49ea3105406752f891a609",
                "plaintext": "Pandas 1.0 came out recently.  To celebrate, here\'s a little tour of what brought us here. There are a lot of places where this story could start, but let\'s start in 1954.  1954 had two events that are pretty important to the birth of Pandas. Castle Bravo Breathe in that whiff of the apocalypseOn March 1st, 1954, the US tested a high-yield thermonuclear bomb on Bikini Atoll.  Lithium deuteride (LiD) was the fuel.  Natural lithium includes two different isotopes - Lithium 6 and Lithium 7.  LiD 6 was understood to be Good H-Bomb Fuel, and LiD 7 was used as a moderating substance in the reaction, on the assumption that it was totally inert.  Turns out that this assumption was extremely wrong - the substance that was supposed to moderate the reaction wound up turning into fuel.  What was supposed to be a 6 megaton blast turned out to be a 15 megaton blast. The consequences of this test are far-reaching, both in time and space.  The crew of a Japanese fishing boat suffered acute radiation poisoning, and many people in the Marshall Islands suffered long term harm from fallout.  It lead to an understanding of what fallout actually was, and that you weren\'t safe from a nuclear blast just from being outside of it - it affected people hundreds of miles away.  Castle Bravo also echoes across culture - it helped inspire Godzilla, and it\'s why Spongebob & friends live in \"Bikini Bottom\" (a reference to Bikini Atoll).  Perhaps most saliently, and most relevant to our story, it was a large motivator behind the 1963 Limited Test Ban Treaty, which ended nuclear testing in the atmosphere, underwater, and in space (though there could still be underground tests).  Castle Bravo made it clear just how dangerous these experiments could be, how widespread the damage could be, and that it was basically impossible to guarantee a lack of major mistakes. Naturally, this meant a major investment in computer technology to simulate nuclear blasts instead of relying so much on tests.  This technology was already in its infancy, but the mandate for simulating nukes would drive scientific computing until the present day.  This drive for computers and software is ultimately where Silicon Valley comes from.  The Department of Defense and Department of Energy\'s hunger for computers, no matter the cost, lead them to buy up every batch of semiconductors until they were cheap enough to be cost-effective for a more general market. Fortran > “Much of my work has come from being lazy.  I didn\'t like writing programs, and so, when I was working on the IBM 701, writing programs for computing missile trajectories, I started work on a programming system to make it easier to write programs.” - John W. Backus That thought process should seem pretty familiar to any Pandas user - it is essentially what\'s motivated Pandas, R, SQL, and basically any other framework that tries to let you focus on declarative programming for math & data manipulation.  Fortran (a portmanteau on \"Formula Translation\") is a tool for writing scientific programs - it may look verbose compared to equivalent Python code, but it\'s certainly a lot more expressive than Assembly.  You can probably follow the code here [https://en.wikipedia.org/wiki/Fortran#Code_examples], which wouldn\'t necessarily be the case with a bunch of Op Codes.  It also has the distinction of being the oldest programming language still in use.  It was developed in 1950, but its first program was run in 1954. Fortran is more than just a spiritual antecedent to scientific computing.  Fortran packages for doing matrix operations, such as BLAS and LAPACK, are \"under the hood\" of Pandas.  The one on your computer isn\'t necessarily written in Fortran - the default is a C translation.  But it\'s an option, where the C one came from, and generally what you want if you really need performance. Note that BLAS, LAPACK, and much of the rest of the scientific Fortran ecosystem remain products of the military-industrial complex.  Or, at least, the ones available open-source.  Organizations like The Department of Energy, DARPA, and the NSF (which has a defense mandate) provide the funding and work hours to keep these packages with fresh updates all the way until today.  And this is part of why it\'s still used - it\'s hard to beat those decades of optimizations. Fortran is only half of our story, however.  Pandas isn\'t just about the fast operations - it\'s also about the syntax. APL from here: https://www.slideshare.net/theburningmonk/fear-and-loathing-with-apl-oredevOkay, Fortran is a step up from assembly, but it\'s not really what NumPy or Pandas code looks like.  For that, we need array-based languages with nice vectorized syntax.  There were a few of these kicking around in the 60s and 70s as an example of Convergent Evolution (including S, the predecessor to R) - but I\'m going to talk about APL because it\'s the weirdest, most theoretically-grounded, and I\'m pretty sure Wes McKinney has gone on-record saying it was an inspiration for Pandas. There\'s a saying that there are two types of programming languages - those that start \"from the computer upwards\", and those that start \"from mathematics downward\".  Fortran, for all its relative user-friendliness, still makes you think about things like pre-allocating memory.  APL came from a mathematician named  Kenneth E. Iverson, who came up with a notation for manipulating arrays.  Eventually they wrote up an implementation in Fortran, and it became a for-real programming language. APL was terse, expressive, and made matrix operations a first-class citizen.  Sure, you had to learn a bunch of weird symbols, will need a custom keyboard, and have to internalize a syntax that includes a concept of \"adverbs\".  But, if all you were doing was manipulating data, then that wasn\'t so bad - it certainly matched the thought process more cleanly than repeated assignment statements or explicitly writing loops.  If you like the Tidyverse, method-chaining in Pandas, or even UNIX-style piping, you like this programming paradigm.  It\'s also closer to mathematical notation, which is nice if you\'re wired a certain way and/or have that background. APL was huge, particularly in finance.  Wrapping your mind around imperative code is weird if your training was in mathematical modeling - APL let bankers focus on their models.  And this is still the case - today APL itself is a novelty for the most part, but it survives in the form of J, Q, and most importantly kdb, mostly used in finance.  And of course, Pandas itself was developed while McKinney was working at the hedge fund 2Sigma. Conclusion Man, the world\'s weird, right? Background Links https://blog.nuclearsecrecy.com/2013/06/21/castle-bravo-revisited/ https://ourcodingclub.github.io/2018/07/30/fortran-intro.html https://www.whoishostingthis.com/resources/apl/",
                "feature_image": "https://cdn.hackersandslackers.com/2020/02/pandas-history-1.jpg",
                "featured": False,
                "status": "published",
                "visibility": "public",
                "email_recipient_filter": "none",
                "created_at": "2020-02-17 01:19:45.000Z",
                "updated_at": "2020-12-10 19:21:14.000Z",
                "published_at": "2020-02-17 12:00:00.000Z",
                "custom_excerpt": "A nuclear test gone wrong, high finance, and some convenient code!",
                "authors": [
                    {
                        "id": "61304d7e74047afda1c21620",
                        "name": "Mister Man",
                        "slug": "man",
                        "email": "fake@example.com",
                        "profile_image": "https://cdn.hackersandslackers.com/authors/mattavi@2x.jpg",
                        "cover_image": "https://cdn.hackersandslackers.com/2020/03/lynxy.jpg",
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
                        "url": "https://hackersandslackers.com/author/matt/",
                    }
                ],
                "tags": [
                    {
                        "id": "61304d8174047afda1c2164b",
                        "name": "Pandas",
                        "slug": "pandas",
                        "description": "Analyze data with the Pandas data analysis library for Python. Start from the basics or see real-life examples of pros using Pandas to solve problems.",
                        "visibility": "public",
                        "meta_title": "Data Analysis with Python & Pandas",
                        "meta_description": "Analyze data with the Pandas data analysis library for Python. Start from the basics or see real-life examples of pros using Pandas to solve problems.",
                        "created_at": "2018-04-16T23:26:05.000Z",
                        "updated_at": "2020-08-04T22:14:59.000Z",
                        "og_title": "Data Analysis with Python & Pandas",
                        "og_description": "Analyze data with the Pandas data analysis library for Python. Start from the basics or see real-life examples of pros using Pandas to solve problems.",
                        "twitter_title": "Data Analysis with Python & Pandas",
                        "twitter_description": "Analyze data with the Pandas data analysis library for Python. Start from the basics or see real-life examples of pros using Pandas to solve problems.",
                        "accent_color": "#ca6094",
                        "url": "https://hackersandslackers.com/tag/pandas/",
                    }
                ],
                "primary_author": {
                    "id": "5dc42cb612c9ce0d63f5bf39",
                    "name": "Mister Man",
                    "slug": "man",
                    "email": "fake@example.com",
                    "profile_image": "https://cdn.hackersandslackers.com/authors/mattavi@2x.jpg",
                    "cover_image": "https://cdn.hackersandslackers.com/2020/03/lynxy.jpg",
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
                            "id": "6dc42c6b4b25bc0d1367444c",
                            "name": "Owner",
                            "description": "Blog Owner",
                            "created_at": "2019-11-07T14:38:35.000Z",
                            "updated_at": "2019-11-07T14:38:35.000Z",
                        }
                    ],
                    "url": "https://hackersandslackers.com/author/matt/",
                },
                "primary_tag": {
                    "id": "61304d8174047afda1c2164b",
                    "name": "Pandas",
                    "slug": "pandas",
                    "description": "Analyze data with the Pandas data analysis library for Python. Start from the basics or see real-life examples of pros using Pandas to solve problems.",
                    "visibility": "public",
                    "meta_title": "Data Analysis with Python & Pandas",
                    "meta_description": "Analyze data with the Pandas data analysis library for Python. Start from the basics or see real-life examples of pros using Pandas to solve problems.",
                    "created_at": "2018-04-16T23:26:05.000Z",
                    "updated_at": "2020-08-04T22:14:59.000Z",
                    "og_title": "Data Analysis with Python & Pandas",
                    "og_description": "Analyze data with the Pandas data analysis library for Python. Start from the basics or see real-life examples of pros using Pandas to solve problems.",
                    "twitter_title": "Data Analysis with Python & Pandas",
                    "twitter_description": "Analyze data with the Pandas data analysis library for Python. Start from the basics or see real-life examples of pros using Pandas to solve problems.",
                    "accent_color": "#ca6094",
                    "url": "https://hackersandslackers.com/tag/pandas/",
                    },
                "url": "https://hackersandslackers.com/a-brief-history-of-pandas/",
                "excerpt": "A nuclear test gone wrong, high finance, and some convenient code!",
                "reading_time": 2,
                "send_email_when_published": False,
                "og_title": "A Brief History of Pandas",
                "og_description": "A nuclear test gone wrong, high finance, and some convenient code!",
                "twitter_title": "A Brief History of Pandas",
                "twitter_description": "A nuclear test gone wrong, high finance, and some convenient code!",
                "meta_title": "A Brief History of Pandas",
                "meta_description": "A nuclear test gone wrong, high finance, and some convenient code!",
            },
            "previous": {},
        }
        # fmt: on


class GhostMember(BaseModel):
    """Ghost Member account."""

    # fmt: off
    id: str
    uuid: str
    email: str
    name: Optional[str]
    note: Optional[str] = None
    subscribed: bool = Field(None, example=True)
    created_at: datetime = Field(None, example="2020-12-20 10:54:20")
    updated_at: datetime = Field(None, example="2020-12-20 10:54:20")
    labels: List[Optional[str]] = Field([], example=["Label1", "Label2"])
    avatar_image: Optional[str] = Field(None, example="https://gravatar.com/avatar/a94833516733d846f03e678a8b4367e9?s=250&d=blank")
    comped: bool = Field(None, example=True)
    # fmt: on


class NewsletterSubscriber(BaseModel):
    """Ghost email subscriber (may not have account)."""

    name: Optional[str] = Field(None, example=None)
    email: str = Field(None, example="fake@example.com")


class EmailSchema(BaseModel):
    """Ghost outgoing email."""

    email: List[EmailStr]
    body: Dict[str, Any]


class GhostSubscriber(BaseModel):
    """Incoming request to update Ghost subscriber"""

    current: Optional[GhostMember]
    previous: Optional[GhostMember]


class Subscription(BaseModel):
    """Ghost email subscription details of a single user."""

    member: GhostSubscriber

    class Config:
        json_schema_extra = {
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
    """Email sent to new Ghost subscribers."""

    from_email: str = Field(None, example="fake@example.com")
    to_email: str = Field(None, example="recipient@example.com")
    subject: str = Field(None, example="Welcome to Hackers & Slackers")
    template: str = Field(None, example="This is an email")

    class Config:
        json_schema_extra = {
            "from_email": "fake@example.com",
            "to_email": "recipient@example.com",
            "subject": "Welcome to Hackers & Slackers",
            "template": "This is an email",
        }


class SMS:
    """Twilio SMS message notification."""

    phone_recipient: str
    phone_sender: str
    date_sent: str
    message: str

    class Config:
        json_schema_extra = {
            "phone_recipient": "5554201738",
            "phone_sender": "5551738420",
            "date_sent": "2020-12-02T02:59:13.642Z",
            "message": "u up?",
        }


class GithubIssue:
    """Newly created Github issue."""

    issue: Dict[str, Any]

    class Config:
        json_schema_extra = {
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


class GithubUser(BaseModel):
    """Github user account."""

    login: str = Field(None, example="dependabot[bot]")
    id: int = Field(None, example=49699333)
    node_id: str = Field(None, example="MDM6Qm90NDk2OTkzMzM=")
    avatar_url: str = Field(None, example="https://avatars.githubusercontent.com/in/29110?v=4")
    gravatar_id: str = Field(None, example="")
    url: str = Field(None, example="https://api.github.com/users/dependabot%5Bbot%5D")
    html_url: str = Field(None, example="https://github.com/apps/dependabot")
    followers_url: str = Field(None, example="https://api.github.com/users/dependabot%5Bbot%5D/followers")
    following_url: str = Field(None, example="https://api.github.com/users/dependabot%5Bbot%5D/following{/other_user}")
    gists_url: str = Field(None, example="https://api.github.com/users/dependabot%5Bbot%5D/gists{/gist_id}")
    starred_url: str = Field(None, example="https://api.github.com/users/dependabot%5Bbot%5D/starred{/owner}{/repo}")
    subscriptions_url: str = Field(None, example="https://api.github.com/users/dependabot%5Bbot%5D/subscriptions")
    organizations_url: str = Field(None, example="https://api.github.com/users/dependabot%5Bbot%5D/orgs")
    repos_url: str = Field(None, example="https://api.github.com/users/dependabot%5Bbot%5D/repos")
    events_url: str = Field(None, example="https://api.github.com/users/dependabot%5Bbot%5D/events{/privacy}")
    received_events_url: str = Field(None, example="https://api.github.com/users/dependabot%5Bbot%5D/received_events")
    type: str = Field(None, example="Bot")
    site_admin: bool = Field(None, example=False)

    class Config:
        json_schema_extra = {
            "login": "dependabot[bot]",
            "id": 49699333,
            "node_id": "MDM6Qm90NDk2OTkzMzM=",
            "avatar_url": "https://avatars.githubusercontent.com/in/29110?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/dependabot%5Bbot%5D",
            "html_url": "https://github.com/apps/dependabot",
            "followers_url": "https://api.github.com/users/dependabot%5Bbot%5D/followers",
            "following_url": "https://api.github.com/users/dependabot%5Bbot%5D/following{/other_user}",
            "gists_url": "https://api.github.com/users/dependabot%5Bbot%5D/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/dependabot%5Bbot%5D/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/dependabot%5Bbot%5D/subscriptions",
            "organizations_url": "https://api.github.com/users/dependabot%5Bbot%5D/orgs",
            "repos_url": "https://api.github.com/users/dependabot%5Bbot%5D/repos",
            "events_url": "https://api.github.com/users/dependabot%5Bbot%5D/events{/privacy}",
            "received_events_url": "https://api.github.com/users/dependabot%5Bbot%5D/received_events",
            "type": "Bot",
            "site_admin": False,
        }


class GithubRepository(BaseModel):
    """Github repository."""

    # fmt: off
    id: int = Field(None, example=245327108)
    node_id: str = Field(None, example="MDEwOlJlcG9zaXRvcnkyNDUzMjcxMDg=")
    name: str = Field(None, example="repository")
    full_name: str = Field(None, example="username/repository")
    private: bool = Field(None, example=False)
    html_url: str = Field(None, example="https://github.com/username/repository")
    description: str = Field(None, example="📑 🎛️ API to automate optimizations for self-hosted blogging platforms.")
    fork: bool = Field(None, example=False)
    url: str = Field(None, example="https://api.github.com/repos/username/repository")
    forks_url: str = Field(None, example="https://api.github.com/repos/username/repository/forks")
    keys_url: str = Field(None, example="https://api.github.com/repos/username/repository/keys{/key_id}")
    collaborators_url: str  = Field(None, example="https://api.github.com/repos/username/repository/collaborators{/collaborator}")
    teams_url: str = Field(None, example="https://api.github.com/repos/username/repository/teams")
    hooks_url: str = Field(None, example="https://api.github.com/repos/username/repository/hooks")
    issue_events_url: str = Field(None, example="https://api.github.com/repos/username/repository/issues/events{/number}")
    events_url: str = Field(None, example="https://api.github.com/repos/username/repository/events")
    assignees_url: str = Field(None, example="https://api.github.com/repos/username/repository/assignees{/user}")
    branches_url: str = Field(None, example="https://api.github.com/repos/username/repository/branches{/branch}")
    tags_url: str = Field(None, example="https://api.github.com/repos/username/repository/tags")
    blobs_url: str = Field(None, example="https://api.github.com/repos/username/repository/git/blobs{/sha}")
    git_tags_url: str = Field(None, example="https://api.github.com/repos/username/repository/git/tags{/sha}")
    git_refs_url: str = Field(None, example="https://api.github.com/repos/username/repository/git/refs{/sha}")
    trees_url: str = Field(None, example="https://api.github.com/repos/username/repository/git/trees{/sha}")
    statuses_url: str = Field(None, example="https://api.github.com/repos/username/repository/statuses/{sha}")
    languages_url: str = Field(None, example="https://api.github.com/repos/username/repository/languages")
    stargazers_url: str = Field(None, example="https://api.github.com/repos/username/repository/stargazers")
    contributors_url: str = Field(None, example="https://api.github.com/repos/username/repository/contributors")
    subscribers_url: str = Field(None, example="https://api.github.com/repos/username/repository/subscribers")
    subscription_url: str = Field(None, example="https://api.github.com/repos/username/repository/subscription")
    commits_url: str = Field(None, example="https://api.github.com/repos/username/repository/commits{/sha}")
    git_commits_url: str = Field(None, example="https://api.github.com/repos/username/repository/git/commits{/sha}")
    comments_url: str = Field(None, example="https://api.github.com/repos/username/repository/comments{/number}")
    issue_comment_url: str = Field(None, example="https://api.github.com/repos/username/repository/issues/comments{/number}")
    contents_url: str = Field(None, example="https://api.github.com/repos/username/repository/contents/{+path}")
    compare_url: str = Field(None, example="https://api.github.com/repos/username/repository/compare/{base}...{head}")
    merges_url: str = Field(None, example="https://api.github.com/repos/username/repository/merges")
    archive_url: str = Field(None, example="https://api.github.com/repos/username/repository/{archive_format}{/ref}")
    downloads_url: str = Field(None, example="https://api.github.com/repos/username/repository/downloads")
    issues_url: str = Field(None, example="https://api.github.com/repos/username/repository/issues{/number}")
    pulls_url: str = Field(None, example="https://api.github.com/repos/username/repository/pulls{/number}")
    milestones_url: str = Field(None, example="https://api.github.com/repos/username/repository/milestones{/number}")
    notifications_url: str = Field(None, example="https://api.github.com/repos/username/repository/notifications{?since,all,participating}")
    labels_url: str = Field(None, example="https://api.github.com/repos/username/repository/labels{/name}")
    releases_url: str = Field(None, example="https://api.github.com/repos/username/repository/releases{/id}")
    deployments_url: str = Field(None, example="https://api.github.com/repos/username/repository/deployments")
    created_at: str = Field(None, example="2020-03-06T04:07:25Z")
    updated_at: str = Field(None, example="2024-01-14T00:01:00Z")
    pushed_at: str = Field(None, example="2024-01-30T00:26:27Z")
    git_url: str = Field(None, example="git://github.com/username/repository.git")
    ssh_url: str = Field(None, example="git@github.com:username/repository.git")
    clone_url: str = Field(None, example="https://github.com/username/repository.git")
    svn_url: str = Field(None, example="https://github.com/username/repository")
    homepage: str = Field(None, example="")
    size: int = Field(None, example=3358)
    stargazers_count: int = Field(None, example=9)
    watchers_count: int = Field(None, example=9)
    language: str = Field(None, example="Python")
    has_issues: bool = Field(None, example=True)
    has_projects: bool = Field(None, example=True)
    has_downloads: bool = Field(None, example=True)
    has_wiki: bool = Field(None, example=True)
    has_pages: bool = Field(None, example=False)
    has_discussions: bool = Field(None, example=False)
    forks_count: int = Field(None, example=1)
    mirror_url: Optional[str]= Field(None, example=None)
    archived: bool = Field(None, example=False)
    disabled: bool = Field(None, example=False)
    open_issues_count: int = Field(None, example=17)
    license: Optional[str]= Field(None, example=None)
    allow_forking: bool = Field(None, example=True)
    is_template: bool = Field(None, example=False)
    web_commit_signoff_required: bool = Field(None, example=False)
    topics: List[Optional[str]] = Field(None, example=["api", "automation", "python"])
    visibility: str = Field(None, example="public")
    forks: int = Field(None, example=1)
    open_issues:int = Field(None, example=17)
    watchers: int = Field(None, example=9)
    default_branch: str = Field(None, example="master")
    # fmt: on


class GithubBranch(BaseModel):
    """Github branch."""

    # fmt: off
    label: str = Field(None, example="toddbirchard:master")
    ref: str = Field(None, example="master")
    sha: str = Field(None, example="67a1fad6e3edba3b581e54c67b42de837ab53726")
    user: GithubUser
    repo: GithubRepository
    # fmt: on


class GithubPrLinks(BaseModel):
    """Github pull request link associations."""

    # fmt: off
    self: dict = Field(None, example={"href": "https://api.github.com/repos/username/repository/pulls/320"})
    html: dict = Field(None, example={"href": "https://github.com/username/repository/pull/320"})
    issue: dict = Field(None, example={"href": "https://api.github.com/repos/username/repository/issues/320"})
    comments: dict = Field(None, example={"href": "https://api.github.com/repos/username/repository/issues/320/comments"})
    review_comments: dict = Field(None, example={"href": "https://api.github.com/repos/username/repository/pulls/320/comments"})
    review_comment: dict = Field(None, example={"href": "https://api.github.com/repos/username/repository/pulls/comments{/number}"})
    commits: dict = Field(None, example={"href": "https://api.github.com/repos/username/repository/pulls/320/commits"})
    statuses: dict = Field(None, example={"href": "https://api.github.com/repos/username/repository/statuses/56e8fc41369d8f6b95c6ab7a206c69cd12bab916"})
    # fmt: on


class GithubPr(BaseModel):
    """Github pull request."""

    # fmt: off
    id: int = Field(None, example=1701068295)
    url: str = Field(None, example="https://api.github.com/repos/username/repository/pulls/320")
    node_id: str = Field(None, example="PR_kwDODp9lBM5lZD4H")
    html_url: str = Field(None, example="https://github.com/username/repository/pull/320")
    diff_url: str = Field(None, example="https://github.com/username/repository/pull/320.diff")
    patch_url: str = Field(None, example="https://github.com/username/repository/pull/320.patch")
    issue_url: str = Field(None, example="https://api.github.com/repos/username/repository/issues/320")
    number: int = Field(None, example=320)
    state: str = Field(None, example="open")
    locked: bool = Field(None, example=False)
    title: str = Field(None, example="Bump aiohttp from 3.9.1 to 3.9.2")
    head: GithubBranch
    user: GithubUser
    base: GithubBranch
    repo: GithubRepository
    body: str = Field(None, example="Bumps [aiohttp](https://github.com/aio-libs/aiohttp) from 3.9.1 to 3.9.2.")
    created_at: str = Field(None, example="2024-01-30T00:26:26Z")
    updated_at: str  = Field(None, example="2024-01-30T00:26:49Z")
    closed_at: Optional[str] = Field(None, example=None)
    merged_at: Optional[str] = Field(None, example=None)
    merge_commit_sha: str = Field(None, example="d5da67d43a36c981d9159007d91c371506b08ca8")
    assignee: Optional[str] = Field(None, example=None)
    assignees: List[Optional[str]] = Field(None, example=[])
    requested_reviewers: List[Optional[str]] = Field(None, example=[])
    requested_teams: List[Optional[str]] = Field(None, example=[])
    labels: dict = Field(None, example={"id": 3075826725, "node_id": "MDU6TGF", "url": "https://api.github.com/repos/username/repository/labels/dependencies", "name": "dependencies", "color": "0366d6", "default": False, "description": "Pull requests that update a dependency file"})
    milestone: Optional[bool] = Field(None, example=None)
    draft: bool = Field(None, example=False)
    commits_url: str = Field(None, example="https://api.github.com/repos/username/repository/pulls/320/commits")
    review_comments_url: str = Field(None, example="https://api.github.com/repos/username/repository/pulls/320/comments")
    review_comment_url: str = Field(None, example="https://api.github.com/repos/username/repository/pulls/comments{/number}")
    comments_url: str = Field(None, example="https://api.github.com/repos/username/repository/issues/320/comments")
    statuses_url: str = Field(None, example="https://api.github.com/repos/username/repository/statuses/56e8fc41369d8f6b95c6ab7a206c69cd12bab916")
    repo: GithubRepository
    _links: GithubPrLinks
    author_association: str = Field(None, example="CONTRIBUTOR")
    auto_merge: Optional[bool] = Field(None, example=None)
    active_lock_reason: Optional[str] = Field(None, example=None)
    merged: bool = Field(None, example=False)
    mergeable: bool = Field(None, example=True)
    rebaseable: bool = Field(None, example=True)
    mergeable_state: str = Field(None, example="unstable")
    merged_by: Optional[str] = Field(None, example=None)
    comments: int = Field(None, example=0)
    review_comments: int = Field(None, example=0)
    maintainer_can_modify: bool = Field(None, example=False)
    commits: int = Field(None, example=1)
    additions: int = Field(None, example=78)
    deletions: int = Field(None, example=78)
    changed_files: int = Field(None, example=1)
    # fmt: on

    class Config:
        """JSON schema example for Github pull request."""

        json_schema_extra = {
            "url": "https://api.github.com/repos/username/repository/pulls/320",
            "id": 1701068295,
            "node_id": "PR_kwDODp9lBM5lZD4H",
            "html_url": "https://github.com/username/repository/pull/320",
            "diff_url": "https://github.com/username/repository/pull/320.diff",
            "patch_url": "https://github.com/username/repository/pull/320.patch",
            "issue_url": "https://api.github.com/repos/username/repository/issues/320",
            "number": 320,
            "state": "open",
            "locked": False,
            "title": "Bump aiohttp from 3.9.1 to 3.9.2",
            "user": {
                "login": "dependabot[bot]",
                "id": 49699333,
                "node_id": "MDM6Qm90NDk2OTkzMzM=",
                "avatar_url": "https://avatars.githubusercontent.com/in/29110?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/dependabot%5Bbot%5D",
                "html_url": "https://github.com/apps/dependabot",
                "followers_url": "https://api.github.com/users/dependabot%5Bbot%5D/followers",
                "following_url": "https://api.github.com/users/dependabot%5Bbot%5D/following{/other_user}",
                "gists_url": "https://api.github.com/users/dependabot%5Bbot%5D/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/dependabot%5Bbot%5D/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/dependabot%5Bbot%5D/subscriptions",
                "organizations_url": "https://api.github.com/users/dependabot%5Bbot%5D/orgs",
                "repos_url": "https://api.github.com/users/dependabot%5Bbot%5D/repos",
                "events_url": "https://api.github.com/users/dependabot%5Bbot%5D/events{/privacy}",
                "received_events_url": "https://api.github.com/users/dependabot%5Bbot%5D/received_events",
                "type": "Bot",
                "site_admin": False,
            },
            "body": 'Bumps [aiohttp](https://github.com/aio-libs/aiohttp) from 3.9.1 to 3.9.2.\n<details>\n<summary>Release notes</summary>\n<p><em>Sourced from <a href="https://github.com/aio-libs/aiohttp/releases">aiohttp\'s releases</a>.</em></p>\n<blockquote>\n<h2>3.9.2</h2>\n<h2>Bug fixes</h2>\n<ul>\n<li>\n<p>Fixed server-side websocket connection leak.</p>\n<p><em>Related issues and pull requests on GitHub:</em>\n<a href="https://redirect.github.com/aio-libs/aiohttp/issues/7978">#7978</a>.</p>\n</li>\n<li>\n<p>Fixed <code>web.FileResponse</code> doing blocking I/O in the event loop.</p>\n<p><em>Related issues and pull requests on GitHub:</em>\n<a href="https://redirect.github.com/aio-libs/aiohttp/issues/8012">#8012</a>.</p>\n</li>\n<li>\n<p>Fixed double compress when compression enabled and compressed file exists in server file responses.</p>\n<p><em>Related issues and pull requests on GitHub:</em>\n<a href="https://redirect.github.com/aio-libs/aiohttp/issues/8014">#8014</a>.</p>\n</li>\n<li>\n<p>Added runtime type check for <code>ClientSession</code> <code>timeout</code> parameter.</p>\n<p><em>Related issues and pull requests on GitHub:</em>\n<a href="https://redirect.github.com/aio-libs/aiohttp/issues/8021">#8021</a>.</p>\n</li>\n<li>\n<p>Fixed an unhandled exception in the Python HTTP parser on header lines starting with a colon -- by :user:<code>pajod</code>.</p>\n<p>Invalid request lines with anything but a dot between the HTTP major and minor version are now rejected.\nInvalid header field names containing question mark or slash are now rejected.\nSuch requests are incompatible with :rfc:<code>9110#section-5.6.2</code> and are not known to be of any legitimate use.</p>\n<p><em>Related issues and pull requests on GitHub:</em>\n<a href="https://redirect.github.com/aio-libs/aiohttp/issues/8074">#8074</a>.</p>\n</li>\n<li>\n<p>Improved validation of paths for static resources requests to the server -- by :user:<code>bdraco</code>.</p>\n</li>\n</ul>\n<!-- raw HTML omitted -->\n</blockquote>\n<p>... (truncated)</p>\n</details>\n<details>\n<summary>Changelog</summary>\n<p><em>Sourced from <a href="https://github.com/aio-libs/aiohttp/blob/master/CHANGES.rst">aiohttp\'s changelog</a>.</em></p>\n<blockquote>\n<h1>3.9.2 (2024-01-28)</h1>\n<h2>Bug fixes</h2>\n<ul>\n<li>\n<p>Fixed server-side websocket connection leak.</p>\n<p><em>Related issues and pull requests on GitHub:</em>\n:issue:<code>7978</code>.</p>\n</li>\n<li>\n<p>Fixed <code>web.FileResponse</code> doing blocking I/O in the event loop.</p>\n<p><em>Related issues and pull requests on GitHub:</em>\n:issue:<code>8012</code>.</p>\n</li>\n<li>\n<p>Fixed double compress when compression enabled and compressed file exists in server file responses.</p>\n<p><em>Related issues and pull requests on GitHub:</em>\n:issue:<code>8014</code>.</p>\n</li>\n<li>\n<p>Added runtime type check for <code>ClientSession</code> <code>timeout</code> parameter.</p>\n<p><em>Related issues and pull requests on GitHub:</em>\n:issue:<code>8021</code>.</p>\n</li>\n<li>\n<p>Fixed an unhandled exception in the Python HTTP parser on header lines starting with a colon -- by :user:<code>pajod</code>.</p>\n<p>Invalid request lines with anything but a dot between the HTTP major and minor version are now rejected.\nInvalid header field names containing question mark or slash are now rejected.\nSuch requests are incompatible with :rfc:<code>9110#section-5.6.2</code> and are not known to be of any legitimate use.</p>\n<p><em>Related issues and pull requests on GitHub:</em>\n:issue:<code>8074</code>.</p>\n</li>\n</ul>\n<!-- raw HTML omitted -->\n</blockquote>\n<p>... (truncated)</p>\n</details>\n<details>\n<summary>Commits</summary>\n<ul>\n<li><a href="https://github.com/aio-libs/aiohttp/commit/24a6d64966d99182e95f5d3a29541ef2fec397ad"><code>24a6d64</code></a> Release v3.9.2 (<a href="https://redirect.github.com/aio-libs/aiohttp/issues/8082">#8082</a>)</li>\n<li><a href="https://github.com/aio-libs/aiohttp/commit/9118a5831e8a65b8c839eb7e4ac983e040ff41df"><code>9118a58</code></a> [PR <a href="https://redirect.github.com/aio-libs/aiohttp/issues/8079">#8079</a>/1c335944 backport][3.9] Validate static paths (<a href="https://redirect.github.com/aio-libs/aiohttp/issues/8080">#8080</a>)</li>\n<li><a href="https://github.com/aio-libs/aiohttp/commit/435ad46e6c26cbf6ed9a38764e9ba8e7441a0e3b"><code>435ad46</code></a> [PR <a href="https://redirect.github.com/aio-libs/aiohttp/issues/3955">#3955</a>/8960063e backport][3.9] Replace all tmpdir fixtures with tmp_path (...</li>\n<li><a href="https://github.com/aio-libs/aiohttp/commit/d33bc21414e283c9e6fe7f6caf69e2ed60d66c82"><code>d33bc21</code></a> Improve validation in HTTP parser (<a href="https://redirect.github.com/aio-libs/aiohttp/issues/8074">#8074</a>) (<a href="https://redirect.github.com/aio-libs/aiohttp/issues/8078">#8078</a>)</li>\n<li><a href="https://github.com/aio-libs/aiohttp/commit/0d945d1be08f2ba8475513216a66411f053c3217"><code>0d945d1</code></a> [PR <a href="https://redirect.github.com/aio-libs/aiohttp/issues/7916">#7916</a>/822fbc74 backport][3.9] Add more information to contributing page (...</li>\n<li><a href="https://github.com/aio-libs/aiohttp/commit/3ec4fa1f0e0a0dad218c75dbe5ed09e22d5cc284"><code>3ec4fa1</code></a> [PR <a href="https://redirect.github.com/aio-libs/aiohttp/issues/8069">#8069</a>/69bbe874 backport][3.9] 📝 Only show changelog draft for non-release...</li>\n<li><a href="https://github.com/aio-libs/aiohttp/commit/419d715c42c46daf1a59e0aff61c1f6d10236982"><code>419d715</code></a> [PR <a href="https://redirect.github.com/aio-libs/aiohttp/issues/8066">#8066</a>/cba34699 backport][3.9] 💅📝 Restructure the changelog for clarity (#...</li>\n<li><a href="https://github.com/aio-libs/aiohttp/commit/a54dab3b36bcf0d815b9244f52ae7bc5da08f387"><code>a54dab3</code></a> [PR <a href="https://redirect.github.com/aio-libs/aiohttp/issues/8049">#8049</a>/a379e634 backport][3.9] Set cause for ClientPayloadError (<a href="https://redirect.github.com/aio-libs/aiohttp/issues/8050">#8050</a>)</li>\n<li><a href="https://github.com/aio-libs/aiohttp/commit/437ac47fe332106a07a2d5335bb89619f1bc23f7"><code>437ac47</code></a> [PR <a href="https://redirect.github.com/aio-libs/aiohttp/issues/7995">#7995</a>/43a5bc50 backport][3.9] Fix examples of <code>fallback_charset_resolver</code>...</li>\n<li><a href="https://github.com/aio-libs/aiohttp/commit/034e5e34ee11c6138c773d85123490e691e1b708"><code>034e5e3</code></a> [PR <a href="https://redirect.github.com/aio-libs/aiohttp/issues/8042">#8042</a>/4b91b530 backport][3.9] Tightening the runtime type check for ssl (...</li>\n<li>Additional commits viewable in <a href="https://github.com/aio-libs/aiohttp/compare/v3.9.1...v3.9.2">compare view</a></li>\n</ul>\n</details>\n<br />\n\n\n[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=aiohttp&package-manager=pip&previous-version=3.9.1&new-version=3.9.2)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)\n\nDependabot will resolve any conflicts with this PR as long as you don\'t alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.\n\n[//]: # (dependabot-automerge-start)\n[//]: # (dependabot-automerge-end)\n\n---\n\n<details>\n<summary>Dependabot commands and options</summary>\n<br />\n\nYou can trigger Dependabot actions by commenting on this PR:\n- `@dependabot rebase` will rebase this PR\n- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it\n- `@dependabot merge` will merge this PR after your CI passes on it\n- `@dependabot squash and merge` will squash and merge this PR after your CI passes on it\n- `@dependabot cancel merge` will cancel a previously requested merge and block automerging\n- `@dependabot reopen` will reopen this PR if it is closed\n- `@dependabot close` will close this PR and stop Dependabot recreating it. You can achieve the same result by closing it manually\n- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency\n- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)\n- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)\n- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)\nYou can disable automated security fix PRs for this repo from the [Security Alerts page](https://github.com/username/repository/network/alerts).\n\n</details>\n\n┆Issue is synchronized with this [Jira Pull Request](https://hackersandslackers.atlassian.net/browse/API-160)\n',
            "created_at": "2024-01-30T00:26:26Z",
            "updated_at": "2024-01-30T00:26:49Z",
            "closed_at": None,
            "merged_at": None,
            "merge_commit_sha": "d5da67d43a36c981d9159007d91c371506b08ca8",
            "assignee": None,
            "assignees": [],
            "requested_reviewers": [],
            "requested_teams": [],
            "labels": [
                {
                    "id": 3075826725,
                    "node_id": "MDU6TGFiZWwzMDc1ODI2NzI1",
                    "url": "https://api.github.com/repos/username/repository/labels/dependencies",
                    "name": "dependencies",
                    "color": "0366d6",
                    "default": False,
                    "description": "Pull requests that update a dependency file",
                }
            ],
            "milestone": None,
            "draft": False,
            "commits_url": "https://api.github.com/repos/username/repository/pulls/320/commits",
            "review_comments_url": "https://api.github.com/repos/username/repository/pulls/320/comments",
            "review_comment_url": "https://api.github.com/repos/username/repository/pulls/comments{/number}",
            "comments_url": "https://api.github.com/repos/username/repository/issues/320/comments",
            "statuses_url": "https://api.github.com/repos/username/repository/statuses/56e8fc41369d8f6b95c6ab7a206c69cd12bab916",
            "head": {
                "label": "toddbirchard:dependabot/pip/aiohttp-3.9.2",
                "ref": "dependabot/pip/aiohttp-3.9.2",
                "sha": "56e8fc41369d8f6b95c6ab7a206c69cd12bab916",
                "user": {
                    "login": "toddbirchard",
                    "id": 2747442,
                    "node_id": "MDQ6VXNlcjI3NDc0NDI=",
                    "avatar_url": "https://avatars.githubusercontent.com/u/2747442?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/username",
                    "html_url": "https://github.com/toddbirchard",
                    "followers_url": "https://api.github.com/users/username/followers",
                    "following_url": "https://api.github.com/users/username/following{/other_user}",
                    "gists_url": "https://api.github.com/users/username/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/username/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/username/subscriptions",
                    "organizations_url": "https://api.github.com/users/username/orgs",
                    "repos_url": "https://api.github.com/users/username/repos",
                    "events_url": "https://api.github.com/users/username/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/username/received_events",
                    "type": "User",
                    "site_admin": False,
                },
                "repo": {
                    "id": 245327108,
                    "node_id": "MDEwOlJlcG9zaXRvcnkyNDUzMjcxMDg=",
                    "name": "blog-webhook-api",
                    "full_name": "username/repository",
                    "private": False,
                    "owner": {
                        "login": "toddbirchard",
                        "id": 2747442,
                        "node_id": "MDQ6VXNlcjI3NDc0NDI=",
                        "avatar_url": "https://avatars.githubusercontent.com/u/2747442?v=4",
                        "gravatar_id": "",
                        "url": "https://api.github.com/users/username",
                        "html_url": "https://github.com/toddbirchard",
                        "followers_url": "https://api.github.com/users/username/followers",
                        "following_url": "https://api.github.com/users/username/following{/other_user}",
                        "gists_url": "https://api.github.com/users/username/gists{/gist_id}",
                        "starred_url": "https://api.github.com/users/username/starred{/owner}{/repo}",
                        "subscriptions_url": "https://api.github.com/users/username/subscriptions",
                        "organizations_url": "https://api.github.com/users/username/orgs",
                        "repos_url": "https://api.github.com/users/username/repos",
                        "events_url": "https://api.github.com/users/username/events{/privacy}",
                        "received_events_url": "https://api.github.com/users/username/received_events",
                        "type": "User",
                        "site_admin": False,
                    },
                    "html_url": "https://github.com/username/repository",
                    "description": "📑 🎛️ API to automate optimizations for self-hosted blogging platforms.",
                    "fork": False,
                    "url": "https://api.github.com/repos/username/repository",
                    "forks_url": "https://api.github.com/repos/username/repository/forks",
                    "keys_url": "https://api.github.com/repos/username/repository/keys{/key_id}",
                    "collaborators_url": "https://api.github.com/repos/username/repository/collaborators{/collaborator}",
                    "teams_url": "https://api.github.com/repos/username/repository/teams",
                    "hooks_url": "https://api.github.com/repos/username/repository/hooks",
                    "issue_events_url": "https://api.github.com/repos/username/repository/issues/events{/number}",
                    "events_url": "https://api.github.com/repos/username/repository/events",
                    "assignees_url": "https://api.github.com/repos/username/repository/assignees{/user}",
                    "branches_url": "https://api.github.com/repos/username/repository/branches{/branch}",
                    "tags_url": "https://api.github.com/repos/username/repository/tags",
                    "blobs_url": "https://api.github.com/repos/username/repository/git/blobs{/sha}",
                    "git_tags_url": "https://api.github.com/repos/username/repository/git/tags{/sha}",
                    "git_refs_url": "https://api.github.com/repos/username/repository/git/refs{/sha}",
                    "trees_url": "https://api.github.com/repos/username/repository/git/trees{/sha}",
                    "statuses_url": "https://api.github.com/repos/username/repository/statuses/{sha}",
                    "languages_url": "https://api.github.com/repos/username/repository/languages",
                    "stargazers_url": "https://api.github.com/repos/username/repository/stargazers",
                    "contributors_url": "https://api.github.com/repos/username/repository/contributors",
                    "subscribers_url": "https://api.github.com/repos/username/repository/subscribers",
                    "subscription_url": "https://api.github.com/repos/username/repository/subscription",
                    "commits_url": "https://api.github.com/repos/username/repository/commits{/sha}",
                    "git_commits_url": "https://api.github.com/repos/username/repository/git/commits{/sha}",
                    "comments_url": "https://api.github.com/repos/username/repository/comments{/number}",
                    "issue_comment_url": "https://api.github.com/repos/username/repository/issues/comments{/number}",
                    "contents_url": "https://api.github.com/repos/username/repository/contents/{+path}",
                    "compare_url": "https://api.github.com/repos/username/repository/compare/{base}...{head}",
                    "merges_url": "https://api.github.com/repos/username/repository/merges",
                    "archive_url": "https://api.github.com/repos/username/repository/{archive_format}{/ref}",
                    "downloads_url": "https://api.github.com/repos/username/repository/downloads",
                    "issues_url": "https://api.github.com/repos/username/repository/issues{/number}",
                    "pulls_url": "https://api.github.com/repos/username/repository/pulls{/number}",
                    "milestones_url": "https://api.github.com/repos/username/repository/milestones{/number}",
                    "notifications_url": "https://api.github.com/repos/username/repository/notifications{?since,all,participating}",
                    "labels_url": "https://api.github.com/repos/username/repository/labels{/name}",
                    "releases_url": "https://api.github.com/repos/username/repository/releases{/id}",
                    "deployments_url": "https://api.github.com/repos/username/repository/deployments",
                    "created_at": "2020-03-06T04:07:25Z",
                    "updated_at": "2024-01-14T00:01:00Z",
                    "pushed_at": "2024-01-30T00:26:27Z",
                    "git_url": "git://github.com/username/repository.git",
                    "ssh_url": "git@github.com:username/repository.git",
                    "clone_url": "https://github.com/username/repository.git",
                    "svn_url": "https://github.com/username/repository",
                    "homepage": "",
                    "size": 3358,
                    "stargazers_count": 9,
                    "watchers_count": 9,
                    "language": "Python",
                    "has_issues": True,
                    "has_projects": True,
                    "has_downloads": True,
                    "has_wiki": True,
                    "has_pages": False,
                    "has_discussions": False,
                    "forks_count": 1,
                    "mirror_url": None,
                    "archived": False,
                    "disabled": False,
                    "open_issues_count": 17,
                    "license": None,
                    "allow_forking": True,
                    "is_template": False,
                    "web_commit_signoff_required": False,
                    "topics": [
                        "api",
                        "automation",
                        "bigquery",
                        "blogging",
                        "ghost",
                        "github-api",
                        "google-cloud-storage",
                        "python",
                        "webhook-api",
                    ],
                    "visibility": "public",
                    "forks": 1,
                    "open_issues": 17,
                    "watchers": 9,
                    "default_branch": "master",
                },
            },
            "base": {
                "label": "toddbirchard:master",
                "ref": "master",
                "sha": "67a1fad6e3edba3b581e54c67b42de837ab53726",
                "user": {
                    "login": "toddbirchard",
                    "id": 2747442,
                    "node_id": "MDQ6VXNlcjI3NDc0NDI=",
                    "avatar_url": "https://avatars.githubusercontent.com/u/2747442?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/username",
                    "html_url": "https://github.com/toddbirchard",
                    "followers_url": "https://api.github.com/users/username/followers",
                    "following_url": "https://api.github.com/users/username/following{/other_user}",
                    "gists_url": "https://api.github.com/users/username/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/username/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/username/subscriptions",
                    "organizations_url": "https://api.github.com/users/username/orgs",
                    "repos_url": "https://api.github.com/users/username/repos",
                    "events_url": "https://api.github.com/users/username/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/username/received_events",
                    "type": "User",
                    "site_admin": False,
                },
                "repo": {
                    "id": 245327108,
                    "node_id": "MDEwOlJlcG9zaXRvcnkyNDUzMjcxMDg=",
                    "name": "blog-webhook-api",
                    "full_name": "username/repository",
                    "private": False,
                    "owner": {
                        "login": "toddbirchard",
                        "id": 2747442,
                        "node_id": "MDQ6VXNlcjI3NDc0NDI=",
                        "avatar_url": "https://avatars.githubusercontent.com/u/2747442?v=4",
                        "gravatar_id": "",
                        "url": "https://api.github.com/users/username",
                        "html_url": "https://github.com/toddbirchard",
                        "followers_url": "https://api.github.com/users/username/followers",
                        "following_url": "https://api.github.com/users/username/following{/other_user}",
                        "gists_url": "https://api.github.com/users/username/gists{/gist_id}",
                        "starred_url": "https://api.github.com/users/username/starred{/owner}{/repo}",
                        "subscriptions_url": "https://api.github.com/users/username/subscriptions",
                        "organizations_url": "https://api.github.com/users/username/orgs",
                        "repos_url": "https://api.github.com/users/username/repos",
                        "events_url": "https://api.github.com/users/username/events{/privacy}",
                        "received_events_url": "https://api.github.com/users/username/received_events",
                        "type": "User",
                        "site_admin": False,
                    },
                    "html_url": "https://github.com/username/repository",
                    "description": "📑 🎛️ API to automate optimizations for self-hosted blogging platforms.",
                    "fork": False,
                    "url": "https://api.github.com/repos/username/repository",
                    "forks_url": "https://api.github.com/repos/username/repository/forks",
                    "keys_url": "https://api.github.com/repos/username/repository/keys{/key_id}",
                    "collaborators_url": "https://api.github.com/repos/username/repository/collaborators{/collaborator}",
                    "teams_url": "https://api.github.com/repos/username/repository/teams",
                    "hooks_url": "https://api.github.com/repos/username/repository/hooks",
                    "issue_events_url": "https://api.github.com/repos/username/repository/issues/events{/number}",
                    "events_url": "https://api.github.com/repos/username/repository/events",
                    "assignees_url": "https://api.github.com/repos/username/repository/assignees{/user}",
                    "branches_url": "https://api.github.com/repos/username/repository/branches{/branch}",
                    "tags_url": "https://api.github.com/repos/username/repository/tags",
                    "blobs_url": "https://api.github.com/repos/username/repository/git/blobs{/sha}",
                    "git_tags_url": "https://api.github.com/repos/username/repository/git/tags{/sha}",
                    "git_refs_url": "https://api.github.com/repos/username/repository/git/refs{/sha}",
                    "trees_url": "https://api.github.com/repos/username/repository/git/trees{/sha}",
                    "statuses_url": "https://api.github.com/repos/username/repository/statuses/{sha}",
                    "languages_url": "https://api.github.com/repos/username/repository/languages",
                    "stargazers_url": "https://api.github.com/repos/username/repository/stargazers",
                    "contributors_url": "https://api.github.com/repos/username/repository/contributors",
                    "subscribers_url": "https://api.github.com/repos/username/repository/subscribers",
                    "subscription_url": "https://api.github.com/repos/username/repository/subscription",
                    "commits_url": "https://api.github.com/repos/username/repository/commits{/sha}",
                    "git_commits_url": "https://api.github.com/repos/username/repository/git/commits{/sha}",
                    "comments_url": "https://api.github.com/repos/username/repository/comments{/number}",
                    "issue_comment_url": "https://api.github.com/repos/username/repository/issues/comments{/number}",
                    "contents_url": "https://api.github.com/repos/username/repository/contents/{+path}",
                    "compare_url": "https://api.github.com/repos/username/repository/compare/{base}...{head}",
                    "merges_url": "https://api.github.com/repos/username/repository/merges",
                    "archive_url": "https://api.github.com/repos/username/repository/{archive_format}{/ref}",
                    "downloads_url": "https://api.github.com/repos/username/repository/downloads",
                    "issues_url": "https://api.github.com/repos/username/repository/issues{/number}",
                    "pulls_url": "https://api.github.com/repos/username/repository/pulls{/number}",
                    "milestones_url": "https://api.github.com/repos/username/repository/milestones{/number}",
                    "notifications_url": "https://api.github.com/repos/username/repository/notifications{?since,all,participating}",
                    "labels_url": "https://api.github.com/repos/username/repository/labels{/name}",
                    "releases_url": "https://api.github.com/repos/username/repository/releases{/id}",
                    "deployments_url": "https://api.github.com/repos/username/repository/deployments",
                    "created_at": "2020-03-06T04:07:25Z",
                    "updated_at": "2024-01-14T00:01:00Z",
                    "pushed_at": "2024-01-30T00:26:27Z",
                    "git_url": "git://github.com/username/repository.git",
                    "ssh_url": "git@github.com:username/repository.git",
                    "clone_url": "https://github.com/username/repository.git",
                    "svn_url": "https://github.com/username/repository",
                    "homepage": "",
                    "size": 3358,
                    "stargazers_count": 9,
                    "watchers_count": 9,
                    "language": "Python",
                    "has_issues": True,
                    "has_projects": True,
                    "has_downloads": True,
                    "has_wiki": True,
                    "has_pages": False,
                    "has_discussions": False,
                    "forks_count": 1,
                    "mirror_url": None,
                    "archived": False,
                    "disabled": False,
                    "open_issues_count": 17,
                    "license": None,
                    "allow_forking": True,
                    "is_template": False,
                    "web_commit_signoff_required": False,
                    "topics": [
                        "api",
                        "automation",
                        "bigquery",
                        "blogging",
                        "ghost",
                        "github-api",
                        "google-cloud-storage",
                        "python",
                        "webhook-api",
                    ],
                    "visibility": "public",
                    "forks": 1,
                    "open_issues": 17,
                    "watchers": 9,
                    "default_branch": "master",
                },
            },
            "_links": {
                "self": {"href": "https://api.github.com/repos/username/repository/pulls/320"},
                "html": {"href": "https://github.com/username/repository/pull/320"},
                "issue": {"href": "https://api.github.com/repos/username/repository/issues/320"},
                "comments": {"href": "https://api.github.com/repos/username/repository/issues/320/comments"},
                "review_comments": {"href": "https://api.github.com/repos/username/repository/pulls/320/comments"},
                "review_comment": {"href": "https://api.github.com/repos/username/repository/pulls/comments{/number}"},
                "commits": {"href": "https://api.github.com/repos/username/repository/pulls/320/commits"},
                "statuses": {
                    "href": "https://api.github.com/repos/username/repository/statuses/56e8fc41369d8f6b95c6ab7a206c69cd12bab916"
                },
            },
            "author_association": "CONTRIBUTOR",
            "auto_merge": None,
            "active_lock_reason": None,
            "merged": False,
            "mergeable": True,
            "rebaseable": True,
            "mergeable_state": "unstable",
            "merged_by": None,
            "comments": 0,
            "review_comments": 0,
            "maintainer_can_modify": False,
            "commits": 1,
            "additions": 78,
            "deletions": 78,
            "changed_files": 1,
        }


class PostBulkUpdate(BaseModel):
    """Request to bulk update Ghost posts."""

    inserted: Dict[str, Any] = Field(None, example={"count": 5, "posts": 10})
    updated: Dict[str, Any] = Field(None, example={"count": 5, "posts": 10})


class AnalyticsResponse(BaseModel):
    """Response to analytics request."""

    # fmt: off
    weekly_stats: Dict[str, Any] = Field(None, example={"count": 2, "rows": [{"my-post-1": 2}, {"my-post-2": 3}]})
    monthly_stats: Dict[str, Any] = Field(None, example={"count": 2, "rows": [{"my-post-1": 2}, {"my-post-2": 3}]})
    # fmt: on
