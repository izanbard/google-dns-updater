from sys import argv

from google.cloud import dns

from .dns_updater import DNSUpdater
from .application import Application
from . import logger

if __name__ == "__main__":
    app = Application(argv[1:])
    if app.update_required:
        logger.info(f"Updating old address {app.dns_state.last_address} to {app.dns_state.address}")
        dns_client = dns.Client(project=app.targets['project_id'], credentials=app.credentials)
        logger.debug(f"Created dns client for project: {app.targets['project_id']}")
        for target in app.targets['target_list']:
            updater = DNSUpdater(dns_client, target['zone'], target['domain'])
            updater.update(app.dns_state)
        logger.debug(f"Total Updates: {app.dns_state.update_count}")
    else:
        logger.debug("No Update")
    app.close()
