from .domain_enum import run as run_domain_enum
from .subdomain_scan import run as run_subdomain_scan
from .osint_collector import run as run_osint
from .network_mapper import run as run_network_map

def run_recon(target: str, config: dict, runner):
    return {
        "domain_enum": run_domain_enum(target, config),
        "subdomains": run_subdomain_scan(target, config),
        "osint": run_osint(target, config)
    }
  
