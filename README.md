# Ghost Blog Automation API

Standalone API to automate tasks upon Gatsby build triggers.


## Endpoints

* GET /metadata: Performs a collection of SQL queries against all posts to clean and fill in missing metadata.
* GET /images: Generates missing retina, mobile, and webp images for all posts.
* POST /lynx: Auto-assign a feature image upon post update, randomly selected from a CDN directory.
* GET /analytics/week: Migrate post analytics from BigQuery to generate "trending this week" widget.
* GET /analytics/month: Migrate post analytics from BigQuery to generate "trending this month" widget.
* POST /members/mixpanel: Create Mixpanel profile for new subscribers.
* GET /searches: Pull top searches from Algolia to generate search suggestions based on popularity.
