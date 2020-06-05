# JAMStack Automation

![Python](https://img.shields.io/badge/python-^3.8-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac)
![Ghost](https://img.shields.io/badge/Ghost-^v3.0.0-lightgrey.svg?longCache=true&style=flat-square&logo=ghost&logoColor=white&colorB=656c82&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/jamstack-automations.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/jamstack-automations/network)

Automation for your JAMStack site to generate optimized image sizes, clean SEO metadata, handle user sign-ups, and much more.


## Endpoints

#### Posts
  * **GET** `/posts/metadata`: Format or fill-in missing metadata for all posts.
  * **GET** `/posts/lynx`: Replace Lynx `<a>` tags with URL targets - not names.
  * **GET** `/posts/backup`: Fetch JSON backup of all blog data.
#### Searches
  * **GET** `/searches/week`: Pull current week's top Algolia searches and save to a database table (used for search suggestions).
  * **GET** `/searches/historical`: Append current week's Algolia searches to a historical table of all searches.
#### Analytics
  * **GET** `/analytics/week`: Migrate site analytics data from BigQuery to MySQL table ("trending this week" widget).
  * **GET** `/analytics/month`: Migrate site analytics data from BigQuery to MySQL table ("trending this month" widget).
#### Images
  * **GET** `/images/transform` Generates missing retina, mobile, and `.webp` images for all posts.
  * **GET** `/images/transform/lynx`: Apply transformations to all Lynx posts.
  * **GET** `/images/lynx`: Assign feature images to all Lynx posts which are missing them.
  * **POST** `/images/transform`: Generates missing image types for a single feature image upon post update.
  * **POST** `/images/lynx`: Auto-assign a random feature image from a CDN upon post update.
#### Members
  * **POST** `/members/mixpanel`: Create Mixpanel profile for new newsletter subscriber.
  * **POST** `/members/newsletter/welcome`: Send welcome email to new newsletter subscribers via Mailgun.
