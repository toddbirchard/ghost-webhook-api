# Ghost Blog Automation API

![Python](https://img.shields.io/badge/python-^3.8-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac)
![Ghost](https://img.shields.io/badge/Ghost-^v3.0.0-lightgrey.svg?longCache=true&style=flat-square&logo=ghost&logoColor=white&colorB=656c82&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/ghost-automation-api.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/ghost-automation-api/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/ghost-automation-api.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/ghost-automation-api/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/ghost-automation-api.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/ghost-automation-api/network)

Standalone API to automate tasks upon Gatsby build triggers.


## Endpoints

* **GET /metadata**: Performs a collection of SQL queries against all posts to clean and fill in missing metadata.
* **GET /images**: Generates missing retina, mobile, and webp images for all posts.
* **POST /lynx**: Auto-assign a feature image upon post update, randomly selected from a CDN directory.
* **GET /analytics/week**: Migrate post analytics from BigQuery to generate "trending this week" widget.
* **GET /analytics/month**: Migrate post analytics from BigQuery to generate "trending this month" widget.
* **POST /members/mixpanel**: Create Mixpanel profile for new subscribers.
* **GET /searches**: Pull top searches from Algolia to generate search suggestions based on popularity.
