"""
Django settings for peFET project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qiducrnmm(4@q27okxd(&kz+r)$9es6cq#6n#ary+=8evm5+(4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'peFET.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'peFET.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'

# TODO: make more specific once done working out hosting
CORS_ALLOW_ALL_ORIGINS = True

JWT_SECRET = b'\xa8\xaeK\x07\xd7$\xe4|\xe4k\x1f#1o\xb9 tmP\x0b\x86U\xb9\xb9\xcd.\xfc\xf0\x0b}x\xcf\x9e\xac:\xd9\xe7\xd5\xd1QS\xfe\xa3\x86\x8e\x1c7Ip4_\xe0\xeb\xb8\x15{\xf4\xda\xda\x1b\x99\xe2V\xb2'

PARTICIPANT_JWT_SECRET = b'\r\xa4l\x1a.4Q\xc6\xd7}\x19\x0f\x00\x83%\xb8\x92o\xb9\xfdW\n^\x7f~"l)\t\xa9\'O]\x08\xc9\xa8\x1a\xacW\x1d\x07\x809\x96^X/\xc8.\x9eq\x15\x9b2\xe8\x8f\r\xc6)\xa4\x1fay\x0e'

QR_JWT_SECRET = b'\xb6\xd5x\xe2*\xc6E\xb4\xa4\xa3\xa6\xffx\xde9\n\xa5Z!\ta9}\xefD\xe0\xeb\xab\xed\x84^\xe3\xcb\xebQ\xb59(h\x9cY\x0c\x9c\xc9\xb3rCQ\x8f&\xcb\x11\x11\xd1\xf9\x13\x0e\xd4\xef\x8a\x8e=\x98;'

SENDGRID_API_KEY = config('SENDGRID_API_KEY')

FRONTEND_URL = 'http://localhost:8080'

MAX_IMAGE_DIMS = 1024

MAX_QR_AGE = 3600
