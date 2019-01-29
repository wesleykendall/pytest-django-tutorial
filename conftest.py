from django.contrib.auth.models import User
from django_dynamic_fixture import G
import pytest
import responses as responses_

###
# The following functions are vendored in from the pytest-responses
# plugin (https://github.com/getsentry/pytest-responses)
# pytest-responses is still waiting on pytest 4 compatibility, so
# the plugin code has been copied here for now
###


def pytest_configure(config):
    """Load the test environment and the test django settings"""
    config.addinivalue_line(
        'markers',
        'withoutresponses: Tests which need access to external domains.'
    )


def pytest_runtest_setup(item):
    if not (item.get_closest_marker('withoutresponses') or item.get_closest_marker('smoketest')):
        responses_.start()


def pytest_runtest_teardown(item):
    if not (item.get_closest_marker('withoutresponses') or item.get_closest_marker('smoketest')):
        try:
            responses_.stop()
            responses_.reset()
        except RuntimeError:
            # patcher was already uninstalled and responses doesnt let us
            # force maintain it
            pass


@pytest.yield_fixture
def responses():
    with responses_.RequestsMock() as rsps:
        yield rsps

###
# End vendoring of pytest-responses
# This code can be removed once https://github.com/getsentry/pytest-responses/pull/9 has been
# deployed to pypi
###


@pytest.fixture
def authenticated_user(client):
    """Create an authenticated user for a test"""
    user = G(User, username='my_username')
    user.set_password('my_password123')
    user.save()
    client.login(username='my_username', password='my_password123')
    return user
