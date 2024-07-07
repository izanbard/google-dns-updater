import json
import os
import pickle
from argparse import ArgumentParser, Namespace
from pathlib import Path

from dns_state import DNSState
from credentials import Credentials


class Application:
    def __init__(self, raw_args: [str]):
        self.raw_args: [str] = raw_args
        self.args: Namespace = self.parse_arguments()
        if Path(self.args.credentials_file).is_file():
            self.credentials = Credentials().get_credentials(Path(self.args.credentials_file))
        else:
            raise FileNotFoundError("Credentials file not found")
        if Path(self.args.targets_file).is_file():
            with open(Path(self.args.targets_file), 'r') as fd:
                self.targets = json.load(fd)
        else:
            raise FileNotFoundError("Targets file not found")
        if Path(self.args.pickle_file).is_file():
            with open(Path(self.args.pickle_file), "rb") as fd:
                self.dns_state = pickle.load(fd)
                self.dns_state.update_my_address()
                self.update_required: bool = self.dns_state.dns_update_required()
        else:
            self.update_required: bool = True
            self.dns_state = DNSState()

    def close(self):
        self.dns_state.last_address = self.dns_state.address
        with open(Path(self.args.pickle_file), "wb") as fd:
            pickle.dump(self.dns_state, fd)

    def parse_arguments(self):
        parser = ArgumentParser()
        parser.add_argument(
            "--credentials_file",
            "-c",
            type=str,
            default=os.environ.get('DNS_UPDATER_CREDENTIALS_FILE', "../creds.json")
        )
        parser.add_argument(
            "--targets_file",
            "-t",
            type=str,
            default=os.environ.get('DNS_UPDATER_TARGETS_FILE', "../targets.json")
        )
        parser.add_argument(
            "--pickle_file",
            "-p",
            type=str,
            default=os.environ.get('DNS_UPDATER_PICKLE_FILE', "../dns_state.pickle")
        )
        return parser.parse_args(self.raw_args)
