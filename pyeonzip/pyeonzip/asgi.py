"""
ASGI config for pyeonzip project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from blacknoise import BlackNoise
from django.core.asgi import get_asgi_application

from pyeonzip import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyeonzip.settings')

application = get_asgi_application()

#appiclation 설정
application = BlackNoise(get_asgi_application())
application.add(settings.BASE_DIR / "static", "/static")