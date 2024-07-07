from ipaddress import IPv4Address, ip_address

from whatismyip import whatismyipv4


class DNSState:
    def __init__(self):
        self.address: IPv4Address = ip_address(whatismyipv4())
        self.last_address: IPv4Address | None = None
        self.update_count: int = 0

    def update_my_address(self):
        self.address: IPv4Address = ip_address(whatismyipv4())

    def dns_update_required(self):
        return self.address != self.last_address
