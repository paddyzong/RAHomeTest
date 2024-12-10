"""
Django settings for RATypeInfer project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from corsheaders.defaults import default_headers
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$d9crf!(n((jf)oyj(1i2$lmgsdi&dqdy2#&tr!c^gk199fjwn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'rest_framework_tus',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rest_framework_tus.middleware.TusMiddleware',
]

ROOT_URLCONF = 'RATypeInfer.urls'

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

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "RATypeInfer.core.exceptions.custom_exception_handler",
}

WSGI_APPLICATION = 'RATypeInfer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 4 * 1024 * 1024 * 1024

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    'https://aabf68860532a45b989e51b09f711f9f-1693294819.ap-southeast-2.elb.amazonaws.com',  # Load Balancer's DNS
    'http://aabf68860532a45b989e51b09f711f9f-1693294819.ap-southeast-2.elb.amazonaws.com',  # Load Balancer's DNS
    'https://dvn1edhbn5oml.cloudfront.net',
    'http://localhost:3000', 
    'http://localhost',
    'http://127.0.0.1:3000',
]

CORS_ALLOWED_ORIGINS = [
    'https://aabf68860532a45b989e51b09f711f9f-1693294819.ap-southeast-2.elb.amazonaws.com',  # Load Balancer's DNS
    'http://aabf68860532a45b989e51b09f711f9f-1693294819.ap-southeast-2.elb.amazonaws.com',  # Load Balancer's DNS
    'https://dvn1edhbn5oml.cloudfront.net',
    'http://localhost:3000',  # Replace with your frontend URL
    'http://localhost',
    'http://127.0.0.1:3000',
]

REDIS_CONFIG = {
    'HOST': os.getenv('REDIS_HOST', 'localhost'),
    'PORT': int(os.getenv('REDIS_PORT', 6379)),
    'DB': int(os.getenv('REDIS_DB', 0)),
    'PASSWORD': os.getenv('REDIS_PASSWORD', None),  # Optional: Redis password
    'SSL': os.getenv('REDIS_SSL', False) == 'True', # Optional: Use SSL if required
}
CORS_ALLOW_HEADERS = list(default_headers) + [
    'Tus-Resumable',
    'Upload-Offset',
    'Upload-Length',
    'Upload-Metadata',
]

CORS_EXPOSE_HEADERS = [
    'Tus-Resumable',
    'Upload-Offset',
    'Upload-Length',
    'Upload-Metadata',
    'Upload-Expires',
    'Location'
]
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# Define the Redis scheme (rediss for SSL, redis for non-SSL)
REDIS_SCHEME = "rediss" if REDIS_CONFIG['SSL'] else "redis"
REDIS_PASSWORD_PART = f":{REDIS_CONFIG['PASSWORD']}@" if REDIS_CONFIG['PASSWORD'] else ""

CELERY_BROKER_URL = f"{REDIS_SCHEME}://{REDIS_PASSWORD_PART}{REDIS_CONFIG['HOST']}:{REDIS_CONFIG['PORT']}/{REDIS_CONFIG['DB']}"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
