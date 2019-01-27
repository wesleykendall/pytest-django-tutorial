from django.conf import settings
import pytest
import requests
from schema import Schema, Use

from apps.meme import img_flip_api


@pytest.mark.smoketest
def test_img_flip_choose_memes_endpoint():
    """
    Verifies that the choose memes endpoint is returning data with an expected structure
    """
    resp = requests.get(img_flip_api.GET_MEMES_ENDPOINT)
    schema = Schema({
        'success': True,
        'data': {
            'memes': [
                {
                    'id': Use(int),
                    'name': str,
                    'url': str,
                    'width': int,
                    'height': int
                }
            ]
        }
    })

    assert resp.status_code == 200
    assert schema.is_valid(resp.json())


@pytest.mark.smoketest
def test_img_flip_create_memes_endpoint():
    """
    Verifies that the create meme endpoint is returning data with an expected structure

    Note: Be sure IMG_FLIP_USER and IMG_FLIP_PASSWORD settings are correct. Run this
    sparingly since it uses resources on imgflip
    """
    # This depends on the "get memes" endpoint functioning
    resp = requests.get(img_flip_api.GET_MEMES_ENDPOINT)
    meme_id = resp.json()['data']['memes'][0]['id']

    # Create a meme from the first meme template
    resp = requests.post(img_flip_api.CREATE_MEME_ENDPOINT, {
        'template_id': meme_id,
        'text0': 'Upper',
        'text1': 'Lower',
        'username': settings.IMG_FLIP_USER,
        'password': settings.IMG_FLIP_PASSWORD
    })
    schema = Schema({
        'success': True,
        'data': {
            'url': str,
            'page_url': str
        }
    })

    assert resp.status_code == 200
    assert schema.is_valid(resp.json())
