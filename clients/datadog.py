"""Datadog logger."""
from datadog import initialize
from datadog import api as datadog


class DataDog:
    """Trace events to Datadog."""

    def __init__(self, api_key: str, app_key: str):
        self.api_key = api_key
        self.app_key = app_key
        return initialize({
            'api_key': self.api_key,
            'app_key': self.app_key
        })

    def test(self):
        """Test function."""
        title = "Something big happened!"
        text = 'And let me tell you all about it here!'
        tags = ['version:1', 'application:web']

        return datadog.Event.create(title=title, text=text, tags=tags)
