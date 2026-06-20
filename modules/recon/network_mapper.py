import ipaddress
from utils.logger import LOGGER

def run(targets: list, config: dict) -> list:
    """Expand CIDR/IP list into valid network targets"""
    mapped = []
    for t in targets:
        try:
            net = ipaddress.ip_network(t, strict=False)
            mapped.extend([str(h) for h in net.hosts()])
        except ValueError:
            mapped.append(t)
    LOGGER.info(f"Mapped to {len(mapped)} live host candidates")
    return mapped
  
