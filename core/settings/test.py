from .default import *  # noqa: F403

list_mid = list(MIDDLEWARE)

list_mid.insert(
    list_mid.index("djangae.contrib.googleauth.middleware.AuthenticationMiddleware"),
    "djangae.contrib.googleauth.middleware.LocalIAPLoginMiddleware",
)

MIDDLEWARE = tuple(list_mid)
