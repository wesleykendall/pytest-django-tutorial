"""
WSGI config for meme_creator project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
# pylint: disable=wrong-import-order
import os
import dotenv


try:
    dotenv.read_dotenv(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
except Exception as e:  # pylint: disable=broad-except
    print(e)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meme_creator.settings')

from configurations.wsgi import get_wsgi_application  # flake8: noqa pylint: disable=wrong-import-position

application = get_wsgi_application()
