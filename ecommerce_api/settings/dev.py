from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-*6jc1nyf3_70^=*hf3itq4c6rrt^-2-m=vhz%z@60)gs^-(p(j'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INSTALLED_APPS += "debug_toolbar",
MIDDLEWARE += "debug_toolbar.middleware.DebugToolbarMiddleware",

INTERNAL_IPS = [
    "127.0.0.1",
]