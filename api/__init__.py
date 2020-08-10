"""Initialize api."""
from flask import Flask


def init_api():
    """Construct the core application."""
    api = Flask(__name__, instance_relative_config=False)
    api.config.from_object('config.Config')
    with api.app_context():
        from api import (
            posts,
            images,
            algolia,
            analytics,
            members,
            authors,
            routes,
            github
        )

        return api
