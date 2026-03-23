from .base import *

SECRET_KEY = "DONT-USE-IN-PROD-local-super-secret-key-dont-use-in-production-NEVER-USE-IN-PROD"
print('IMPORTED LOCAL SETTINGS')
print('!!!LOCAL SECRET KEY IS BEING USED!!!')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'
