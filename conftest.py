from django.contrib.auth.models import User
from django_dynamic_fixture import G
import pytest
import responses as responses_


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


@pytest.fixture
def authenticated_user(client):
    """Create an authenticated user for a test"""
    user = G(User, username='my_username')
    user.set_password('my_password123')
    user.save()
    client.login(username='my_username', password='my_password123')
    return user
