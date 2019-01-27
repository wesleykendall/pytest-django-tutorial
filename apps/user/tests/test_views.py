import datetime as dt

from django import urls
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django_dynamic_fixture import G
import freezegun
import pytest


@pytest.mark.parametrize('view_name', ['user:register', 'user:login'])
def test_public_views(view_name, client):
    """
    Verify that the registration and login views are publicly accessible
    """
    url = urls.reverse(view_name)
    resp = client.get(url)
    assert resp.status_code == 200


@freezegun.freeze_time('2019-01-26 7:00:00')
@pytest.mark.django_db
def test_register(client):
    """Registers a user and verifies their last login date is correct"""
    register_url = urls.reverse('user:register')
    resp = client.post(register_url, {
        'username': 'my_username',
        'password1': 'my_password123',
        'password2': 'my_password123'
    })

    # The registration view should redirect us to our home page
    assert resp.status_code == 302
    assert resp.url == urls.reverse('home')

    # There should be a user with 'my_username'
    user = User.objects.get(username='my_username')
    # The user's last login time should be set to the current time
    assert user.last_login == dt.datetime(2019, 1, 26, 7)


@pytest.mark.django_db
def test_login_and_logout(client):
    """Tests logging in and logging out"""
    # Create a fake user
    user = G(User, username='my_username')
    user.set_password('my_password123')
    user.save()

    login_url = urls.reverse('user:login')
    resp = client.post(login_url, {
        'username': 'my_username',
        'password': 'my_password123'
    })

    # The login url should redirect to the home page
    assert resp.status_code == 302
    assert resp.url == urls.reverse('home')

    # Logged in users have a session created for them
    assert Session.objects.count() == 1

    # Log out the user
    logout_url = urls.reverse('user:logout')
    resp = client.get(logout_url)

    # Similar to the login view, the logout view redirects to the login page
    assert resp.status_code == 302
    assert resp.url == urls.reverse('user:login')

    # There should be no more sessions left after logging out
    assert not Session.objects.exists()
