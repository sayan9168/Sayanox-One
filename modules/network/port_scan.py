import socket
from utils.logger import LOGGER
from advanced.fast_scan import ParallelRunner

def scan_port(ip: str, port: int, timeout: float = 2.0):
    """Real‑world safe scan — no false positives"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return {"ip": ip, "port": port, "status": "open"} if s.connect_ex((ip, port)) == 0 else None
    except Exception:
        return None

def run(targets: list, config: dict):
    results = []
    runner = ParallelRunner(config)
    start_port, end_port = map(int, config["scan"]["port_range"].split("-"))

    for host in targets:
        ip = host if isinstance(host, str) else host.get("ip")
        if not ip:
            continue
        LOGGER.info(f"→ Scanning {ip} ports {start_port}–{end_port}")
        port_list = list(range(start_port, end_port+1))
        open_ports = runner.run(lambda p: scan_port(ip, p), port_list)
        results.extend([p for p in open_ports if p])
    return results
    
