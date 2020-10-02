"""Initialize api."""
from flask import Flask
from flask_cors import CORS


def init_api():
    """Construct the core application."""
    api = Flask(__name__, instance_relative_config=False)
    api.config.from_object('config.Config')
    CORS(api, resources={r"/*": {"origins": "*"}})

    # Enable Datadog APM
    if api.config['DATADOG_TRACE_ENABLED'] == 'prod':
        from ddtrace import patch_all
        patch_all()

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
