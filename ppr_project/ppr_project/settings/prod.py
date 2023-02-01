import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .common import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ['ks-45.ru', 'www.ks-45.ru', 'localhost', 'web']
CSRF_TRUSTED_ORIGINS = ['https://*.ks-45.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

STATIC_ROOT = BASE_DIR / 'static'

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],

    traces_sample_rate=1.0,

    send_default_pii=True
)
