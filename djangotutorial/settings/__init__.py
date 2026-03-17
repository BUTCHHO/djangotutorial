
from .base import *

DJANGO_ENV_TYPE = environ.get('DJANGO_ENV_TYPE')
print('django env type:', DJANGO_ENV_TYPE)
if DJANGO_ENV_TYPE == 'local':
    from .local import *
elif DJANGO_ENV_TYPE == 'production':
    from .production import *