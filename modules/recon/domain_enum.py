import dns.resolver
from utils.logger import LOGGER

def run(target: str, config: dict) -> dict:
    """Fetch all standard DNS records"""
    records = {}
    types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]
    resolver = dns.resolver.Resolver()
    resolver.timeout = config["general"]["timeout"] / 1000

    for rtype in types:
        try:
            ans = resolver.resolve(target, rtype)
            records[rtype] = [str(r) for r in ans]
        except Exception as e:
            LOGGER.debug(f"{rtype} record error: {e}")
            records[rtype] = []
    return {"domain": target, "dns_records": records}
  
