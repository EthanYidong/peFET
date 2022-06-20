from pathlib import Path

from decouple import config

from .common import *

DEBUG = False

ALLOWED_HOSTS = ['api.pefet.blender.eu.org']

SECRET_KEY = config('DJANGO_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOWED_ORIGINS = [
    'https://pefet.blender.eu.org',
]

FRONTEND_URL = 'http://localhost:8080'

JWT_SECRET = config('JWT_SECRET', cast=lambda k: bytes(k, "utf-8"))

PARTICIPANT_JWT_SECRET = config('PARTICIPANT_JWT_SECRET', cast=lambda k: bytes(k, "utf-8"))

QR_JWT_SECRET = config('QR_JWT_SECRET', cast=lambda k: bytes(k, "utf-8"))
