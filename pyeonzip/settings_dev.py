from .settings import *
import os
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# DB 관련 세팅
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}