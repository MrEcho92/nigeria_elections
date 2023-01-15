from djangae.contrib.secrets import get
from django.urls.base import reverse_lazy

from core.secrets import Secrets

from .default import *  # noqa: F403

ALLOWED_HOSTS = [
    "*",
]

APP_SECRETS = get(Secrets)
SECRET_KEY = APP_SECRETS.secret_key

# Disable DEBUG on production
DEBUG = False

# Strip out middleware only designed for local development
_LOCAL_ONLY_MIDDLEWARE = (
    "djangae.contrib.googleauth.middleware.LocalIAPLoginMiddleware",
)

MIDDLEWARE = [x for x in MIDDLEWARE if x not in _LOCAL_ONLY_MIDDLEWARE]


# Enable secure settings

SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 2592000  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True

SECURE_REDIRECT_EXEMPT = [
    # App Engine doesn't use HTTPS internally, so the /_ah/.* URLs need to be exempt.
    # Django compares these to request.path.lstrip("/"), hence the lack of preceding /
    r"^_ah/"
]

LOGIN_URL = reverse_lazy("googleauth_oauth2login")
LOGIN_REDIRECT_URL = "/"

# Enable JWT by setting
GOOGLEAUTH_IAP_JWT_ENABLED = True

GOOGLEAUTH_CLIENT_ID = (
    "1068316479168-1rpf02l9i0c5v598764rhls71ieu59t3.apps.googleusercontent.com"
)
GOOGLEAUTH_CLIENT_SECRET = APP_SECRETS.google_oauth_client_secret

# CSP Configuration

CSP_REPORT_ONLY = False


# Un-comment if using cache with Cloud Memory Store memcache. For LOCATION use
# the 'Discovery endpoint' value for the instance.
# CACHES = {
#    "default": {
#        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
#        "LOCATION": "x.x.x.x:11211",
#    }
# }
