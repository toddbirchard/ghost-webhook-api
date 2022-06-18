# JAMStack Automation

![Python](https://img.shields.io/badge/Python-^3.9-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![FastAPI](https://img.shields.io/badge/FastAPI-^v0.75.2-blue.svg?longCache=true&logo=fastapi&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![PyDantic](https://img.shields.io/badge/Pydantic-^v1.9.0-blue.svg?longCache=true&logo=python&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Google Cloud](https://img.shields.io/badge/Google--Cloud-^v0.34.0-lightgrey.svg?longCache=true&style=flat-square&logo=googlecloud&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Ghost](https://img.shields.io/badge/Ghost-^v4.0.0-lightgrey.svg?longCache=true&style=flat-square&logo=ghost&logoColor=white&colorB=656c82&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/network)

![Jamstack Automation API](./.github/jamstack@2x.png)

API to consume JAMStack webhook actions. Dynamically handles optimizations including image compression, content sanitation, alerting, and feature enablement via data aggregate (suggested searches, trending posts, etc)

## Endpoints

#### Posts

Endpoints to guarantee published posts have proper metadata & embedded URLs.

  * **GET** `/posts/`: Bulk update metadata for all posts where applicable. Supports meta titles, og titles & descriptions, and feature images.
  * **POST** `/posts/`: Populate metadata for a single post upon publish. Supports meta title, og title & description, and feature image.
  * **GET** `/posts/backup`: Fetch JSON backup of all blog data
  
#### Analytics

Aggregate data from Google Cloud & Algolia to power “trending” widgets.

  * **GET** `/analytics/`: Export site analytics from a data warehouse to a SQL database. Useful for trend-related features ie: "trending this week" widget.
  * **GET** `/analytics/searches/`: Fetch top Algolia search queries for the current week. Export results to a “trending searches” SQL table, as well as historical searches.
  
#### Image Optimization

Ensure all posts have retina, mobile, and webp variants. 

  * **POST** `/images/`: Upon post creation, generate optimized retina and mobile variants of post ‘feature_image’ if they do not exist.
  * **GET** `/images/`: Generates both **retina** and **mobile** varieties of _all_ images in a remote CDN directory. Defaults to directory containing images uploaded within current month, or accepts a `?directory=` parameter which accepts a path to recursively optimize images on the given CDN.
  * **GET** `/images/sort`: Transverses CDN in a given directory (`?directory=`) to organize images into subdirectories based on image type (retina or mobile).

#### Accounts

Handle user account creation & interactions.

  * **POST** `/account/`: Create Ghost member from Netlify Auth service (supports auth providers Github, Google, etc.)
  * **POST** `/account/comment/`: Accept user-submitted comments for posts. Each submission notifies the post’s author via a Mailgun email.
  * **POST** `/account/comment/upvote/`: Increment (or de increment) a comment’s upvote count by 1, with maximum 1 vote per user.

#### Donate

  * **POST** `/donation/`: Adds [BuyMeACoffee](https://www.buymeacoffee.com/hackersslackers) donation to a historical ledger.
  * **DELETE** `/donation/`: Delete a [BuyMeACoffee](https://www.buymeacoffee.com/hackersslackers) donation from historical ledger.
  * **GET** `/donation/`: Get all [BuyMeACoffee](https://www.buymeacoffee.com/hackersslackers) donations.


#### Newsletter

Logistics of adding or removing newsletter subscriptions.

  * **POST** `/subscription/`: Send welcome email to newsletter subscribers via Mailgun.
  * **DELETE** `/subscription/`: Track newsletter unsubscribe events.

#### Authors

Insight to scenarios where Authors likely need assistance.

 * **GET** `/authors/updated/`: Update all authors to have correct CDN urls & sanitized metadata.
 * **POST** `/authors/post/created/`: Notify site editor when posts are ready for review
 * **POST** `/authors/post/updated/`: Notify original post author when a peer edits a post.

#### Github

Notifications when user activity is made on project repos.

  *  **POST** `/github/pr/`: Trigger SMS notification when contributors open a Github PR in a specified Github org.
  *  **POST** `/github/issue/`: Trigger SMS notification when contributors open a Github issue in a specified Github org.

### Installation

Get up and running with `make deploy`:

```shell
$ git clone https://github.com/toddbirchard/jamstack-api.git
$ cd jamstack-api
$ make deploy
``` 
