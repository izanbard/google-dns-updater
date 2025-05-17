from ipaddress import IPv4Address, ip_address

from whatismyip import whatismyipv4
from . import logger

class DNSState:
    def __init__(self):
        self.address: IPv4Address = ip_address(whatismyipv4())
        self.last_address: IPv4Address | None = None
        self.update_count: int = 0

    def update_my_address(self):
        self.address: IPv4Address = ip_address(whatismyipv4())

    def dns_update_required(self):
        update_required = self.address != self.last_address
        if update_required:
            logger.debug(f"My IP address {self.address} is different to stored IP address {self.last_address}")
        return self.address != self.last_address
