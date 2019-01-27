"""
Django settings for meme_creator project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
# pylint: disable=no-init
import datetime as dt
import os

from configurations import Configuration, values
import dj_database_url


class Common(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = values.ListValue([])
    SECRET_KEY = values.SecretValue()

    # Project and company-specific settings
    PROJECT_NAME = values.Value('meme_creator')
    PROTOCOL = values.Value('https')
    HOST = values.SecretValue()
    TOP_LEVEL_HOST = values.Value('meme_creator.me')

    # Application definition
    INSTALLED_APPS = [
        # Django apps
        'whitenoise.runserver_nostatic',  # Must include first

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.humanize',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.staticfiles',

        # Third party apps
        'bootstrap4',
        'django_extensions',
        'stronghold',
        'webpack_loader',

        # Internal apps
        'apps.marketing',
        'apps.meme',
        'apps.user',
        'meme_creator',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'stronghold.middleware.LoginRequiredMiddleware',
    ]

    ROOT_URLCONF = 'meme_creator.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'meme_creator.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases
    DATABASES = {
        'default': dj_database_url.config(),
    }

    # Authentication
    LOGIN_URL = '/user/login/'
    LOGIN_REDIRECT_URL = '/'

    # Password validation
    # https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/2.0/topics/i18n/
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = False

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.1/howto/static-files/
    STATIC_URL = '/static/'
    STATIC_ROOT = 'staticfiles'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'src'),
    )
    # Cache static files for one year. It is assumed we hash every static file
    WHITENOISE_MAX_AGE = 31536000

    # Webpack
    WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': 'dist/',
            'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        }
    }

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    }


class Test(Common):
    """
    Test settings

    Note: test settings are loaded in the root conftest file after
    reading in the .env.template environment file. This is to allow
    running ``pytest`` directly without having to do ``python manage.py test``.
    """

    # Make default values for unsupported field types in Djano dynamic fixture
    DDF_FIELD_FIXTURES = {
        'django.db.models.fields.DurationField': lambda: dt.timedelta(minutes=30),
    }
    DDF_FILL_NULLABLE_FIELDS = values.BooleanValue(False)


class Development(Test):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    ALLOWED_HOSTS = values.ListValue(['localhost', '127.0.0.1', '.ngrok.io'])

    INTERNAL_IPS = [
        '127.0.0.1'
    ]

    INSTALLED_APPS = Common.INSTALLED_APPS + ['debug_toolbar']

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]


class Staging(Common):
    """
    The in-staging settings.
    """
    # Security
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_REDIRECT_EXEMPT = values.ListValue([])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(
        ('HTTP_X_FORWARDED_PROTO', 'https')
    )
    CSRF_COOKIE_SECURE = values.BooleanValue(True)
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_PRELOAD = values.BooleanValue(True)


class Production(Staging):
    """
    The in-production settings.
    """
    pass
