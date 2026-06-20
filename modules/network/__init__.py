from .port_scan import run as scan_ports
from .service_probe import run as probe_services
from .mitm_check import run as check_tls

def run_network_scan(targets, config, runner):
    results = {}
    for host in targets:
        ports = scan_ports([host], config)
        open_ports = [p["port"] for p in ports if p["status"] == "Open"]
        results[host] = {
            "open_ports": open_ports,
            "services": probe_services(host, open_ports),
            "tls_info": check_tls(host) if 443 in open_ports else {}
        }
    return results
  
