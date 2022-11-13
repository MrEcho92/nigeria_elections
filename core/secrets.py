from dataclasses import dataclass

from djangae.contrib.secrets import DefaultSecrets


@dataclass
class Secrets(DefaultSecrets):
    google_oauth_client_secret: str = ""
