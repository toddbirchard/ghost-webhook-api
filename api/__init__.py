"""Initialize api."""
from flask import Flask
from flask_cors import CORS
from ddtrace import patch_all
patch_all()


def init_api():
    """Construct the core application."""
    api = Flask(__name__, instance_relative_config=False)
    api.config.from_object('config.Config')
    CORS(api, resources={r"/*": {"origins": "*"}})
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
