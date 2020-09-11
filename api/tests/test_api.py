from flask import url_for
import pytest


@pytest.mark.usefixtures('client_class')
class TestSuite:

    def test_api(self):
        assert self.client.get(url_for('health_check')).status_code == 200
