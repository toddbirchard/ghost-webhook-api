"""Initialize api."""
from flask import Flask
from clients.database import Database


db = Database()


def init_api():
    """Construct the core application."""
    api = Flask(__name__, instance_relative_config=False)
    api.config.from_object('config.Config')
    db.init_app(api)

    with api.app_context():
        db.create_all()
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
