from sys import argv

from google.cloud import dns

from .dns_updater import DNSUpdater
from .application import Application
from . import logger

if __name__ == "__main__":
    app = Application(argv[1:])
    if app.update_required:
        logger.info("...Update Required...")
        dns_client = dns.Client(project=app.targets['project_id'], credentials=app.credentials)
        for target in app.targets['target_list']:
            updater = DNSUpdater(dns_client, target['zone'], target['domain'])
            updater.update(app.dns_state)
        logger.info(f"...Total Updates: {app.dns_state.update_count}...")
    else:
        logger.info("...Update Not Required...")
    app.close()
