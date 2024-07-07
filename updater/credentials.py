from pathlib import Path

from google.oauth2 import service_account


class Credentials:
    def __init__(self):
        self.credentials = None

    def get_credentials(self, credentials_file: Path):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_file)
        return self.credentials
