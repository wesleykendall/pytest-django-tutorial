import datetime as dt

from bs4 import BeautifulSoup
from django import urls
from django_dynamic_fixture import G
import pytest

from apps.meme import img_flip_api
import apps.meme.models as meme_models


@pytest.mark.parametrize('url_name, url_kwargs', [
    ('meme:memes', None),
    ('meme:choose', None),
    ('meme:create', {'id': 1234, 'url': 'https://meme.com'})
])
def test_protected_views(client, url_name, url_kwargs):
    """Verify meme views are protected from unauthenticated access"""
    url = urls.reverse(url_name, kwargs=url_kwargs)
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url.startswith(urls.reverse('user:login'))


@pytest.mark.django_db
def test_choose_and_create_meme(authenticated_user, client, mocker):
    """Tests the entire flow of choosing and creating a meme"""

    # Make the get_memes function return an API response
    mocker.patch('apps.meme.img_flip_api.get_memes', autospec=True, return_value=[{
        'id': '1234',
        'url': 'https://memeurl.com/path'
    }])

    # Patch the returned meme url when the meme is created
    mocker.patch('apps.meme.img_flip_api.create_meme', autospec=True,
                 return_value='https://memeurl.com/created')

    # The "choose meme" page should have a meme with "meme_id"
    choose_meme_url = urls.reverse('meme:choose')
    resp = client.get(choose_meme_url)

    soup = BeautifulSoup(resp.content, 'html.parser')
    assert resp.status_code == 200
    assert len(soup.select('.choose-meme-link')) == 1

    # Parse the meme creation link and go to it
    meme_creation_link = soup.select('.choose-meme-link')[0]['href']
    resp = client.get(meme_creation_link)
    assert resp.status_code == 200

    # Create a meme
    resp = client.post(meme_creation_link, {
        'upper_text': 'Hello',
        'lower_text': 'World'
    })
    assert resp.status_code == 302
    assert resp.url == urls.reverse('meme:memes')

    # Verify the meme exists for the authenticated user based on our mocked response
    assert meme_models.Meme.objects.count() == 1
    assert (
        meme_models.Meme.objects
        .filter(user=authenticated_user,
                url='https://memeurl.com/created')
        .exists()
    )


@pytest.mark.django_db
def test_choose_meme_api_error(authenticated_user, client, mocker):
    """Tests choosing a meme when the img flip API returns an error"""
    # Make the get_memes function throw an API error
    mocker.patch('apps.meme.img_flip_api.get_memes',
                 autospec=True,
                 side_effect=img_flip_api.ImgFlipError('API Error!'))

    # Try rendering the "choose memes" page
    choose_meme_url = urls.reverse('meme:choose')
    resp = client.get(choose_meme_url)

    # The page should render file, but it should display an error
    assert resp.status_code == 200
    assert b'Woops! Looks like we\'re having issues' in resp.content


@pytest.mark.django_db
def test_create_meme_api_error(authenticated_user, client, mocker):
    """Tests creating a meme when the img flip API returns an error"""
    # Make the get_memes function throw an API error
    mocker.patch('apps.meme.img_flip_api.create_meme',
                 autospec=True,
                 side_effect=img_flip_api.ImgFlipError('API Error!'))

    # Try creating a meme
    create_meme_url = urls.reverse('meme:create', kwargs={'id': 1234, 'url': 'https://meme.com'})
    resp = client.post(create_meme_url, {
        'upper_text': 'Hello',
        'lower_text': 'World'
    })

    # The page should render fine, but it should be the form page displaying the API error
    assert resp.status_code == 200
    assert b'API Error!' in resp.content


@pytest.mark.django_db
def test_view_memes(authenticated_user, client):
    """Tests viewing memes of an authenticated user"""

    # Make some memes associated with the authenticated user
    G(meme_models.Meme,
      user=authenticated_user,
      creation_time=dt.datetime(2018, 4, 11),
      url='https://memes.com/meme1.jpg')
    G(meme_models.Meme,
      user=authenticated_user,
      creation_time=dt.datetime(2018, 4, 12),
      url='https://memes.com/meme2.jpg')

    # Make some memes for other users to help ensure the
    # meme page is only showing the memes of the auehtnciated
    # user
    G(meme_models.Meme)
    G(meme_models.Meme)

    # Render the meme page for the authenticated user
    show_memes_url = urls.reverse('meme:memes')
    resp = client.get(show_memes_url)

    soup = BeautifulSoup(resp.content, 'html.parser')
    assert resp.status_code == 200
    assert len(soup.select('.meme-img')) == 2

    # Verify that memes are rendered in reverse chronological order
    meme_urls = [img['src'] for img in soup.select('.meme-img')]
    assert meme_urls == ['https://memes.com/meme2.jpg', 'https://memes.com/meme1.jpg']


@pytest.mark.django_db
def test_view_memes_none_created(authenticated_user, client):
    """Tests viewing memes of an authenticated user when no memes have been created"""

    # Render the meme page for the authenticated user
    show_memes_url = urls.reverse('meme:memes')
    resp = client.get(show_memes_url)

    soup = BeautifulSoup(resp.content, 'html.parser')
    assert resp.status_code == 200
    assert not soup.select('.meme-img')
    assert b'You haven\'t created any memes yet!' in resp.content
