# JAMStack Automation

![Python](https://img.shields.io/badge/Python-^3.8-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![FastAPI](https://img.shields.io/badge/FastAPI-^v0.62.0-blue.svg?longCache=true&logo=fastapi&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![PyDantic](https://img.shields.io/badge/Pydantic-^v1.7.3-blue.svg?longCache=true&logo=python&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Ghost](https://img.shields.io/badge/Ghost-^v3.0.0-lightgrey.svg?longCache=true&style=flat-square&logo=ghost&logoColor=white&colorB=656c82&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/network)

![Jamstack Automation API](./.github/jamstack@2x.png)

REST API to provide JAMStack-based sites content & image optimization automation, features from third-party services (Mailgun, Twilio, Github, etc), and data pipelines to power data-driven features. Plays nicely with Webhooks typical of JAMStack sites to trigger a myriad of jobs to empower JAMStack sites.


## Endpoints

#### Posts
  * **GET** `/posts`: Populate metadata for all posts en masse. Supports meta titles, og titles & descriptions, and feature images.
  * **POST** `/posts`: Populate metadata for a single post upon publish. Supports meta title, og title & description, and feature image where applicable.
  * **GET** `/posts/backup`: Fetch JSON backup of all blog data
  * **GET** `/posts/embed`: Batch update all Lynx posts missing embedded link previews.
  * **POST** `/posts/embed`: Replace HTML anchor tags with rich-content link embeds for a given post upon publish.
  * **GET** `/posts/alt`: Batch update all posts with `<img>` tags missing an `alt` attribute.
#### Analytics
  * **GET** `/analytics/`: Export site analytics from a data warehouse to a SQL database. Useful for trend-related features ie: "trending this week" widget.
  * **GET** `/analytics/searches/week`: Fetch top Algolia search queries for the current week and save to an SQL database (useful for building search-related features, ie: search suggestions).
  * **GET** `/analytics/searches/historical`: Fetch top Algolia search queries for the current week and save to an SQL database (non-destructive export intended for historical records).
#### Image Optimization
  * **POST** `/images`: Generate retina and mobile feature_image for a single post upon update.
  * **GET** `/images`: Generates both **retina** and **mobile** varieties of _all_ images in a remote CDN directory. Defaults to directory containing images uploaded within current month, or accepts a `?directory=` parameter which accepts a path to recursively optimize images on the given CDN.
  * **GET** `/images/lynx`: Assign feature images to all Lynx posts which are missing them.
  * **GET** `/images/sort`: Transverses CDN in a given directory (`?directory=`) to organize images into subdirectories based on image type (retina, mobile, etc).
#### Accounts
  * **POST** `/account`: Create Ghost member from Netlify Auth service (supports auth providers Github, Google, etc.)
  * **POST** `/account/comment`: Accept user-submitted comments for posts. Each submission notifies the post’s author via a Mailgun email.
  * **POST** `/account/donation`: Adds BuyMeACoffee donations to a historical ledger.
#### Newsletter
  * **POST** `/subscription`: Send welcome email to newsletter subscribers via Mailgun.
  * **DELETE** `/subscription`: Track newsletter unsubscribe events.
#### Authors
  * **POST** `/authors/post/created`: Notify site admin/editor when posts are ready for review.
  * **POST** `/authors/post/update`: Notify admin user when another author modifies their post.
#### Github
  *  **POST** `/github/pr`: Trigger SMS notification when contributors open a Github PR in a specified Github org.
  *  **POST** `/github/issue`: Trigger SMS notification when contributors open a Github issue in a specified Github org.

### Installation

Get up and running with `make deploy`:

```shell
$ git clone https://github.com/toddbirchard/jamstack-api.git
$ cd jamstack-api
$ make deploy
``` 
