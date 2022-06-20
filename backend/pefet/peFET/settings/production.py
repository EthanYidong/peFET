from pathlib import Path

from decouple import config

from .common import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

SECRET_KEY = config('DJANGO_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOWED_ORIGINS = [
    'https://pefet.blender.eu.org',
    'https://www.pefet.blender.eu.org',
]

CORS_ALLOW_HEADERS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://*.blender.eu.org']

FRONTEND_URL = 'https://pefet.blender.eu.org'

JWT_SECRET = config('JWT_SECRET', cast=lambda k: bytes(k, "utf-8"))

PARTICIPANT_JWT_SECRET = config(
    'PARTICIPANT_JWT_SECRET', cast=lambda k: bytes(k, "utf-8"))

QR_JWT_SECRET = config('QR_JWT_SECRET', cast=lambda k: bytes(k, "utf-8"))
