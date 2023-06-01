from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, EmailStr, Field


class NewDonation(BaseModel):
    # fmt: off
    name: str = Field(None, example="Fake Todd")
    email: str = Field(None, example="fake@example.com")
    count: int = Field(None, example=5)
    message: Optional[str] = Field(None, example="Great tutorials but this is a test message.")
    link: str = Field(None, example="https://buymeacoffee.com/hackersslackers/c/fake")
    coffee_id: int = Field(None, example=3453543)
    # fmt: on

    class Config:
        schema_extra = {
            "name": "Fake Todd",
            "email": "fake@example.com",
            "count": 1,
            "message": "Great tutorials but this is a test message.",
            "link": "https://buymeacoffee.com/hackersslackers",
            "coffee_id": 405127,
        }


class NewComment(BaseModel):
    # fmt: off
    post_id: str = Field(None, example="61304d8374047afda1c2168b")
    post_slug: str = Field(None, example="python-virtualenv-virtualenvwrapper")
    user_id: str = Field(None, example="677f9417-16ab-4d8e-9bed-1130da250c88")
    user_name: Optional[str] = Field(None, example="Todd Birchard")
    user_avatar: Optional[str] = Field(None, example="https://hackersandslackers-cdn.storage.googleapis.com/2021/09/avimoji.jpg")
    user_email: str = Field(None, example="todd@hackersandslackers.com")
    author_name: str = Field(None, example="Todd Birchard")
    author_id: str = Field(None, example="1")
    body: Optional[str] = Field(None, example="These tutorials are awesome! 10/10")
    # fmt: on

    class Config:
        schema_extra = {
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
    comment_id: int = Field(None, example=1)
    user_id: str = Field(None, example="8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385")
    vote: bool = Field(None, example=True)


class Role(BaseModel):
    id: str = Field(None, example="5dc42c6b4b25bc0d13674448")
    name: str = Field(None, example="Administrator")
    description: str = Field(None, example="Administrators")
    created_at: datetime = Field(None, example=datetime.now())
    created_by: str = Field(None, example=1)
    updated_at: datetime = Field(None, example=1)
    updated_by: str = Field(None, example=datetime.now())


class Author(BaseModel):
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
    current: Tag
    previous: Optional[Tag]


class BasePost(BaseModel):
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
    current: BasePost
    previous: Optional[BasePost]


class FetchedPost(BaseModel):
    posts: List[BasePost]


class PostUpdate(BaseModel):
    post: Post

    class Config:
        # fmt: off
        schema_extra = {
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
                        "url": "https://hackersandslackers.app/author/matt/",
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
                    "url": "https://hackersandslackers.app/author/matt/",
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


class NetlifyUserMetadata(BaseModel):
    avatar_url: Optional[str] = Field(None, example="https://example.com/dsfdsf.jpg")
    full_name: str = Field(None, example="Fake Name")
    roles: Optional[List[str]] = Field(None, example=["admin"])


class NetlifyUserAppMetadata(BaseModel):
    provider: str = Field(None, example="google")


class NetlifyAccount(BaseModel):
    id: str = Field(None, example="4e7c4f1b-e51a-4abb-8a58-105483724713")
    aud: str = Field(None, example="")
    email: str = Field(None, example="fake@example.com")
    role: Optional[str] = Field(None, example="Moderator")
    app_metadata: NetlifyUserAppMetadata
    user_metadata: NetlifyUserMetadata
    created_at: str = Field(None, example="2021-03-06T13:26:56.991731Z")
    updated_at: str = Field(None, example="2021-03-06T14:26:56.991731Z")

    class Config:
        schema_extra = {
            "id": "4e7c4f1b-e51a-4abb-8a58-105483724713",
            "aud": "",
            "email": "fake@example.com",
            "role": "Moderator",
            "app_metadata": {"provider": "google"},
            "user_metadata": {
                "avatar_url": "https://example.com/dsfdsf.jpg",
                "full_name": "Fake Name",
                "roles": ["admin"],
            },
            "created_at": "2021-03-06T14:26:56.991731Z",
            "updated_at": "2021-03-06T14:26:56.994492Z",
        }


class NetlifyUserEvent(BaseModel):
    event: str = Field(None, example="signup")
    instance_id: str = Field(None, example="725df7e1-94b8-4b0f-8d45-dc710d8d1a47")
    user: NetlifyAccount


class GhostMember(BaseModel):
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


class NetlifyAccountCreationResponse(BaseModel):
    succeeded: Union[NetlifyUserEvent, None]
    failed: Union[NetlifyUserEvent, None]


class NewsletterSubscriber(BaseModel):
    name: Optional[str] = Field(None, example=None)
    email: str = Field(None, example="fake@example.com")


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]


class GhostSubscriber(BaseModel):
    current: Optional[GhostMember]
    previous: Optional[GhostMember]


class Subscription(BaseModel):
    member: GhostSubscriber

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
    from_email: str = Field(None, example="fake@example.com")
    to_email: str = Field(None, example="recipient@example.com")
    subject: str = Field(None, example="Welcome to Hackers & Slackers")
    template: str = Field(None, example="This is an email")

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


class PostBulkUpdate(BaseModel):
    inserted: Dict[str, Any] = Field(None, example={"count": 5, "posts": 10})
    updated: Dict[str, Any] = Field(None, example={"count": 5, "posts": 10})


class AnalyticsResponse(BaseModel):
    # fmt: off
    weekly_stats: Dict[str, Any] = Field(None, example={"count": 2, "rows": [{"my-post-1": 2}, {"my-post-2": 3}]})
    monthly_stats: Dict[str, Any] = Field(None, example={"count": 2, "rows": [{"my-post-1": 2}, {"my-post-2": 3}]})
    # fmt: on
