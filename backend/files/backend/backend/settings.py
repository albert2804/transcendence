"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


from custom_auth.models import Intra42OAuth2
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0q20k#atx@vql74=j^5=hijw2@=+s0e4gv4wnltw--94#-*yi='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Set allowed hosts from environment variable
ALLOWED_HOSTS = os.environ['DOMAIN'].split()
# Set trusted origins for CSRF from environment variable
CSRF_TRUSTED_ORIGINS = ['https://' + host for host in os.environ['DOMAIN'].split()]

# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'social_django',
    'custom_auth',
    'users',
    'api',
    'chat',
	'remote_game'
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

ASGI_APPLICATION = 'backend.asgi.application'

# Database (PostgreSQL from db-container)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': 'db',
        'PORT': '5432',
    }
}

# use custom user model for authentication
AUTH_USER_MODEL = 'api.CustomUser'

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

# Social Auth config for OAuth
# https://python-social-auth.readthedocs.io/en/latest/configuration/django.html

SOCIAL_AUTH_JSONFIELD_ENABLED = True

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'endpoint/static/'
STATIC_ROOT = BASE_DIR / '../../static'

# directory where media for example (.jpg)is stored
MEDIA_URL = '/endpoint/media/'
MEDIA_ROOT = BASE_DIR / '../../media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Use X-Forwarded-Host and X-Forwarded-Port headers because of reverse proxy
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    #
    #'social_core.backends.open_id.OpenIdAuth',
    #'social_core.backends.google.GoogleOpenId',     #deprecated, remove after testing
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    #'social_core.backends.google.GoogleOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.oauth.BaseOAuth2',
    'custom_auth.models.Intra42OAuth2'
]

SOCIAL_AUTH_GITHUB_KEY='e989ab105c9b8c40d3f6'
SOCIAL_AUTH_GITHUB_SECRET='9a6ca7f1e6106dccf4564dc626fa43c4167e1aeb'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_URL = 'auth/login/'
LOGIN_REDIRECT_URL='/endpoint/auth'

SOCIAL_AUTH_PIPELINE = (
    'custom_auth.models.Intra42OAuth2.foo'
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
#    'custom_auth.pipeline',  # <--- set the path to the function
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

#  LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'default': {
#             'format': '[DJANGO] %(levelname)s %(asctime)s %(module)s '
#                       '%(name)s.%(funcName)s:%(lineno)s: %(message)s'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'default',
#         }
#     },
#     'loggers': {
#         '': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         }
#     },
# }