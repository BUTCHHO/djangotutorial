from os import environ

from .base import *

DJANGO_ENV_TYPE = environ.get('DJANGO_ENV_TYPE')
if DJANGO_ENV_TYPE == 'production':
    print('Loading production settings')
    from .production import *
else:
    from .local import *