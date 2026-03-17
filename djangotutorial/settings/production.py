
from .base import *
print('IMPORTED PRODUCTION')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = environ.get('DJANGO_ALLOWED_HOSTS', "127.0.0.1").split(",")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DATABASE_NAME'),
        'USER': environ.get('DATABASE_USERNAME'),
        'PASSWORD': environ.get('DATABASE_PASSWORD'),
        'HOST': environ.get('DATABASE_HOST'),
        'PORT': environ.get('DATABASE_PORT'),
    }
}
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'