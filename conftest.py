from django.contrib.auth.models import User
from django_dynamic_fixture import G
import pytest


@pytest.fixture
def authenticated_user(client):
    """Create an authenticated user for a test"""
    user = G(User, username='my_username')
    user.set_password('my_password123')
    user.save()
    client.login(username='my_username', password='my_password123')
    return user
