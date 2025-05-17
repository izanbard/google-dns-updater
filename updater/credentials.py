from pathlib import Path

from google.oauth2 import service_account
from . import logger


class Credentials:
    def __init__(self):
        self.credentials = None

    def get_credentials(self, credentials_file: Path):
        if self.credentials is None:
            logger.debug(f"Getting service account credentials from credentials file: {credentials_file}")
            self.credentials = service_account.Credentials.from_service_account_file(credentials_file)
        return self.credentials
