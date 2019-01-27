import urllib.parse

from django.conf import settings
import pytest

from apps.meme import img_flip_api


def test_get_memes_success(responses):
    """Test a successful response of getting memes"""
    memes = [
        {
            'id': '61579',
            'name': 'One Does Not Simply',
            'url': 'https://i.imgflip.com/1bij.jpg',
            'width': 568,
            'height': 335
        },
        {
            'id': '101470',
            'name': 'Ancient Aliens',
            'url': 'https://i.imgflip.com/26am.jpg',
            'width': 500,
            'height': 437
        }
    ]

    # Add the response to the image flip API
    responses.add(responses.GET, img_flip_api.GET_MEMES_ENDPOINT, status=200, json={
        'success': True,
        'data': {
            'memes': memes
        }
    })
    assert img_flip_api.get_memes() == memes


@pytest.mark.parametrize('api_status, api_response', [
    (200, {'success': False}),
    (500, None)
])
def test_get_memes_failure(api_status, api_response, responses):
    """
    Verify an ImgFlipError is raised on successful (200) responses with an unsuccessful body
    and when the API is returning non successful responses
    """
    responses.add(responses.GET, img_flip_api.GET_MEMES_ENDPOINT, status=api_status, json=api_response)
    with pytest.raises(img_flip_api.ImgFlipError):
        img_flip_api.get_memes()


def test_create_meme_success(responses):
    """Tests successfully creating a meme"""
    meme_url = 'https://i.imgflip.com/123abc.jpg'

    # Add the response to the image flip API
    responses.add(responses.POST, img_flip_api.CREATE_MEME_ENDPOINT, status=200, json={
        'success': True,
        'data': {
            'url': 'https://i.imgflip.com/123abc.jpg',
            'page_url': 'https://imgflip.com/i/123abc'
        }
    })

    assert img_flip_api.create_meme('meme_id', 'upper text', 'lower text') == meme_url

    # Verify that we sent the proper request to the img flip API
    assert len(responses.calls) == 1
    posted_data = urllib.parse.parse_qs(responses.calls[0].request.body)
    assert posted_data == {
        'template_id': ['meme_id'],
        'username': [settings.IMG_FLIP_USER],
        'password': [settings.IMG_FLIP_PASSWORD],
        'text0': ['upper text'],
        'text1': ['lower text']
    }


@pytest.mark.parametrize('api_status, api_response', [
    (200, {'success': False, 'error_message': 'Error!'}),
    (500, None)
])
def test_create_meme_error(api_status, api_response, responses):
    """Verify errors are thrown when receiving bad meme creation responses"""
    responses.add(responses.POST, img_flip_api.CREATE_MEME_ENDPOINT, status=api_status, json=api_response)
    with pytest.raises(img_flip_api.ImgFlipError):
        img_flip_api.create_meme('meme_id', 'upper text', 'lower text')
