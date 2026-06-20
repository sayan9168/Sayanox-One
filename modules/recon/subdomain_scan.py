import dns.resolver
from utils.logger import LOGGER

def run(target: str, config: dict):
    """Find all subdomains via DNS + certificate transparency"""
    found = []
    wordlist = open(config["recon"]["subdomain_wordlist"]).read().splitlines()
    resolver = dns.resolver.Resolver()

    for name in wordlist:
        try:
            fqdn = f"{name}.{target}"
            resolver.resolve(fqdn, "A")
            found.append(fqdn)
        except dns.resolver.NXDOMAIN:
            continue
        except Exception as e:
            LOGGER.debug(f"Res error: {e}")
    return {"subdomains": found, "count": len(found)}
  
