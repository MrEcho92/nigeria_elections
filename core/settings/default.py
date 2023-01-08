"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

from djangae.contrib.secrets import get
from djangae.environment import project_id
from djangae.settings_base import *  # noqa

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get().secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "djangae.contrib.googleauth",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djangae",
    "djangae.tasks",
    "djangae.contrib.security",
    # Apps
    "core",
    "poll",
    "public",
]

MIDDLEWARE = [
    "djangae.contrib.common.middleware.RequestStorageMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "djangae.contrib.googleauth.middleware.LocalIAPLoginMiddleware",
    "djangae.contrib.googleauth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATASTORE_INDEX_YAML = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "dsindex.yaml"
)

DATABASES = {
    "default": {
        "ENGINE": "gcloudc.db.backends.datastore",
        "PROJECT": project_id(default="core"),
        "INDEXES_FILE": DATASTORE_INDEX_YAML,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Enable the Djangae IAP backend, but not Django's username/password one by default
AUTHENTICATION_BACKENDS = (
    "djangae.contrib.googleauth.backends.iap.IAPBackend",
    "djangae.contrib.googleauth.backends.oauth2.OAuthBackend",
)

AUTH_USER_MODEL = "core.User"


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "static"))

# Djangae Specific settings

# Set this to the location where your app is deployed.
# Available on the App Engine dashboard.
CLOUD_TASKS_LOCATION = "europe-west"


# CSP Configuration
# https://django-csp.readthedocs.io/en/latest/configuration.html

CSP_REPORT_ONLY = True

CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = (
    "'self'",
    "https://cdnjs.cloudflare.com",
    "https://fonts.googleapis.com",
)
CSP_FONT_SRC = (
    "'self'",
    "https://fonts.googleapis.com",
    "https://fonts.gstatic.com",
)
CSP_FRAME_SRC = ("'self'",)
CSP_CHILD_SRC = ("'self'",)
CSP_SCRIPT_SRC = (
    "'self'",
    "https://cdnjs.cloudflare.com",
)
CSP_IMG_SRC = ("'self'",)
CSP_MEDIA_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_INCLUDE_NONCE_IN = ["script-src"]

LOGIN_URL = "/_dj/login/"

# Security
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True

GOOGLEAUTH_OAUTH_SCOPES = ["openid", "profile", "email"]
GOOGLEAUTH_CLIENT_ID = "xx"
GOOGLEAUTH_CLIENT_SECRET = "xx"

# Geolocation
GEOIP_PATH = Path("geolocation")
