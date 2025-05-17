import json
import os
import pickle
from argparse import ArgumentParser, Namespace
from pathlib import Path

from .dns_state import DNSState
from .credentials import Credentials
from . import logger

class Application:
    def __init__(self, raw_args: [str]):
        self.raw_args: [str] = raw_args
        self.args: Namespace = self.parse_arguments()
        logger.debug(f"Parsed Arguments: {self.args}")
        if Path(self.args.credentials_file).is_file():
            self.credentials = Credentials().get_credentials(Path(self.args.credentials_file))
        else:
            logger.warn(f"No credentials file found at {Path(self.args.credentials_file)}")
            raise FileNotFoundError("Credentials file not found")
        if Path(self.args.targets_file).is_file():
            with open(Path(self.args.targets_file), 'r') as fd:
                self.targets = json.load(fd)
                logger.debug(f"Loaded targets file {Path(self.args.targets_file)}")
        else:
            logger.warn(f"No targets file found at {Path(self.args.targets_file)}")
            raise FileNotFoundError("Targets file not found")
        if Path(self.args.pickle_file).is_file():
            with open(Path(self.args.pickle_file), "rb") as fd:
                self.dns_state = pickle.load(fd)
                self.dns_state.update_my_address()
                self.update_required: bool = self.dns_state.dns_update_required()
                logger.debug(f"Loaded dns state from {self.args.pickle_file}")
        else:
            logger.warn(f"No pickle file found at {Path(self.args.pickle_file)}, starting from scratch")
            self.update_required: bool = True
            self.dns_state = DNSState()

    def close(self):
        self.dns_state.last_address = self.dns_state.address
        logger.debug(f"Check complete, closing. current dns state: {self.dns_state.last_address}")
        with open(Path(self.args.pickle_file), "wb") as fd:
            pickle.dump(self.dns_state, fd)

    def parse_arguments(self):
        parser = ArgumentParser()
        parser.add_argument(
            "--credentials_file",
            "-c",
            type=str,
            default=os.environ.get('DNS_UPDATER_CREDENTIALS_FILE', "./creds.json")
        )
        parser.add_argument(
            "--targets_file",
            "-t",
            type=str,
            default=os.environ.get('DNS_UPDATER_TARGETS_FILE', "./targets.json")
        )
        parser.add_argument(
            "--pickle_file",
            "-p",
            type=str,
            default=os.environ.get('DNS_UPDATER_PICKLE_FILE', "./dns_state.pickle")
        )
        return parser.parse_args(self.raw_args)
