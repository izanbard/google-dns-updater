from time import sleep

from .dns_state import DNSState
from . import logger

class DNSUpdater(object):
    TIME_TO_LIVE = 360

    def __init__(self, client, zone: str, host: str):
        self.client = client
        self.host = host
        self.zone = self.client.zone(zone, host)
        self.changes = self.zone.changes()
        self.records = self.zone.list_resource_record_sets(max_results=100, client=self.client)
        logger.debug(f"Created Updater for zone {self.zone.name}, host {self.host}")

    def update(self, state: DNSState):
        change_to_make: bool = False
        for record in self.records:
            if record.name == self.host and record.record_type == 'A':
                for data in record.rrdatas:
                    if data != state.address:
                        logger.debug(f"Old record: {record.name}, {record.record_type}, {self.TIME_TO_LIVE}, {data.data}")
                        self.changes.delete_record_set(record)
                        self.changes.add_record_set(
                            self.zone.resource_record_set(
                                self.host,
                                record.record_type,
                                self.TIME_TO_LIVE,
                                [str(state.address)]
                            )
                        )
                        logger.debug(f"New record: {self.host}, {record.record_type}, {self.TIME_TO_LIVE}, {state.address}")
                        change_to_make = True

        if change_to_make:
            state.update_count += 1
            self.changes.create()
            while self.changes.status != 'done':
                sleep(2)
                self.changes.reload()
            logger.info(f"Changes are {self.changes.status}")
