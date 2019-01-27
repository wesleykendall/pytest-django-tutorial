from django.conf import settings
import requests


GET_MEMES_ENDPOINT = 'https://api.imgflip.com/get_memes'
CREATE_MEME_ENDPOINT = 'https://api.imgflip.com/caption_image'


class ImgFlipError(Exception):
    pass


def get_memes():
    resp = requests.get(GET_MEMES_ENDPOINT)
    if resp.status_code == 200:
        content = resp.json()
        if content['success']:
            return content['data']['memes']

    raise ImgFlipError('Image Flip API Request Failed')


def create_meme(template_id, upper_text, lower_text):
    resp = requests.post(CREATE_MEME_ENDPOINT, data={
        'template_id': template_id,
        'username': settings.IMG_FLIP_USER,
        'password': settings.IMG_FLIP_PASSWORD,
        'text0': upper_text,
        'text1': lower_text
    })
    if resp.status_code == 200:
        content = resp.json()
        if content['success']:
            return content['data']['url']
        else:
            raise ImgFlipError(content['error_message'])

    raise ImgFlipError('Image Flip API Request Failed')
