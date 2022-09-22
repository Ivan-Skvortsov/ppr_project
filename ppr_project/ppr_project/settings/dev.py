from .common import *  # noqa

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    'debug_toolbar'
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: True,
}

STATIC_ROOT = None
