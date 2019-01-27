import os

import configurations
import dotenv


def pytest_configure():
    """Load the test environment and the test django settings"""
    dotenv.read_dotenv('.env.template')

    os.environ['DJANGO_CONFIGURATION'] = 'Test'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meme_creator.settings'
    configurations.setup()
