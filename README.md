# JAMStack Automation

![Python](https://img.shields.io/badge/Python-^3.8-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Flask](https://img.shields.io/badge/Flask-^v1.1.2-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Ghost](https://img.shields.io/badge/Ghost-^v3.0.0-lightgrey.svg?longCache=true&style=flat-square&logo=ghost&logoColor=white&colorB=656c82&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/network)

![Jamstack Automation API](./.github/jamstack@2x.png)

Python API to provide JAMStack-based sites content & image optimization automation, features from third-party services (Mailgun, Twilio, Github, etc), and data pipelines to power data-driven features. Plays nicely with Webhooks typical of JAMStack sites to trigger a myriad of jobs to empower JAMStack sites.


## Endpoints

#### Posts
  * **GET** `/posts/update`: Populate metadata for all posts en masse. Supports meta titles, og titles & descriptions, and feature images.
  * **POST** `/posts/update`: Populate metadata for a single post upon publish. Supports meta title, og title & description, and feature image where applicable.
  * **GET** `/posts/backup`: Fetch JSON backup of all blog data.
  * **POST** `/posts/embed`: Replace HTML anchor tags with rich-content link embeds for a given post upon publish.
#### Searches
  * **GET** `/searches/week`: Pull current week's top Algolia search queries and save to a SQL database (useful for building search-related features, ie: search suggestions).
  * **GET** `/searches/historical`: Export current month's search queries to a SQL database (non-destructive export intended for historical table of searches).
#### Analytics
  * **GET** `/analytics/week`: Export site analytics from a data warehouse to a SQL database. Useful for trend-related features ie: "trending this week" widget.
  * **GET** `/analytics/month`: Export site analytics from data warehouse to a SQL database.
#### Image Optimization
  * **GET** `/images/transform`: Generates retina and mobile varieties of _all_ post feature_images. Defaults to images uploaded within the current month, or accepts a `?directory=` parameter which accepts a path to recursively optimize images on the given CDN.
  * **POST** `/image/transform`: Generate retina and mobile feature_image for a single post upon update.
  * **GET** `/images/transform/lynx`: Apply transformations to all Lynx posts.
  * **GET** `/images/purge`: Delete unwanted images such as duplicates, unused images, etc.
  * **GET** `/images/mobile`: Generate mobile image variations of post feature_images. Defaults to images uploaded within the current month, or accepts a `?directory=` parameter which accepts a path to recursively optimize images on the given CDN.
  * **GET** `/images/assign/lynx`: Assign feature images to all Lynx posts which are missing them.
#### Members
  * **POST** `/members/signup`: Create Ghost member. Accepts payloads from auth providers to allow sign up via Github, Google, etc.
  * **POST** `/members/mixpanel`: Create Mixpanel profile for new newsletter subscriber.
  * **POST** `/members/newsletter/welcome`: Send welcome email to new newsletter subscribers via Mailgun.
  * **POST** `/members/donation`: Add incoming donation to a historical ledger of donations from BuyMeACoffee.
#### Authors
  * **POST** `/authors/posts/created`: Notify site admin/editor when posts are ready for review.
#### Github
  *  **POST** `/github/pr`: Trigger SMS notification when contributors open a Github PR in a specified Github org.
  *  **POST** `/github/issue`: Trigger SMS notification when contributors open a Github issue in a specified Github org.

## Installation

**Installation via `requirements.txt`**:

```shell
$ git clone https://github.com/toddbirchard/jamstack-automations.git
$ cd jamstack-automations
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip3 install -r requirements.txt
$ python3 main.py
```

**Installation via [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)**:

```shell
$ git clone https://github.com/toddbirchard/jamstack-automations.git
$ cd jamstack-automations
$ pipenv shell
$ pipenv update
$ python3 main.py
```

**Installation via [Poetry](https://python-poetry.org/)**:

```shell
$ git clone https://github.com/toddbirchard/jamstack-automations.git
$ cd jamstack-automations
$ poetry shell
$ poetry update
$ poetry run
```
