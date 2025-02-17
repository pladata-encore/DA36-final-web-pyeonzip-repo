from .settings import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    'Eb-pyeonzip-app-env.eba-skazjekk.ap-northeast-2.elasticbeanstalk.com',
    'pyeonzip.store'
]

# DB 관련 세팅
<<<<<<< HEAD
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME_PROD'),
        'USER': os.getenv('DB_USER_PROD'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST_PROD'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}
=======
>>>>>>> 1cb3ce2caaf804e20a891e7399d7d810434d1a73
