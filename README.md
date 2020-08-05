# JAMStack Automation

![Python](https://img.shields.io/badge/Python-^3.8-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Flask](https://img.shields.io/badge/Flask-1.1.2-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Ghost](https://img.shields.io/badge/Ghost-^v3.0.0-lightgrey.svg?longCache=true&style=flat-square&logo=ghost&logoColor=white&colorB=656c82&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/network)

![Jamstack Automation API](https://github.com/toddbirchard/jamstack-automations/blob/master/.github/jamstack@2x.png)

Supplementary API to optimize JAMStack sites via webhooks. Listens for site updates to clean metadata, optimize images, handle user sign-ups, and much more.


## Endpoints

#### Posts
  * **GET** `/post/all/metadata`: Fill in missing metadata for all posts (titles, descriptions, etc.)
  * **GET** `/post/backup`: Fetch JSON backup of all blog data.
  * **POST** `/post/metadata`: Fill in missing metadata for a single post upon publish (titles, descriptions, etc.)
  * **POST** `/post/lynx/previews`: Replace HTML anchor tags with rich-content link embeds.
#### Searches
  * **GET** `/searches/week`: Pull current week's top Algolia searches and save to a database table (used for search suggestions).
  * **GET** `/searches/historical`: Append current week's Algolia searches to a historical table of all searches.
#### Analytics
  * **GET** `/analytics/week`: Migrate site analytics data from BigQuery to MySQL table ("trending this week" widget).
  * **GET** `/analytics/month`: Migrate site analytics data from BigQuery to MySQL table ("trending this month" widget).
#### Images
  * **GET** `/images/transform`: Generates missing retina, mobile, and *.webp* images for all posts published in the current month. Accepts a *?directory=* parameter to force transformations for images in other directories.
  * **GET** `/images/transform/lynx`: Apply transformations to all Lynx posts.
  * **GET** `/images/assign/lynx`: Assign feature images to all Lynx posts which are missing them.
  * **POST** `/image/transform`: Generates retina feature image for single post upon update. 
#### Members
  * **POST** `/members/mixpanel`: Create Mixpanel profile for new newsletter subscriber.
  * **POST** `/members/newsletter/welcome`: Send welcome email to new newsletter subscribers via Mailgun.
#### Authors
  * **POST** `/authors/posts/created`: Notify site admin/editor when posts are ready for review.
  
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
