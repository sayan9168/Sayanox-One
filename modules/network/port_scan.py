import socket
from concurrent.futures import ThreadPoolExecutor
from advanced.fast_scan import ParallelRunner
from utils.logger import LOGGER

def scan_port(ip: str, port: int, timeout: int = 5) -> dict:
    """Scan a single port on a target IP"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            if result == 0:
                return {"ip": ip, "port": port, "status": "Open"}
    except Exception as e:
        LOGGER.debug(f"Port scan error on {ip}:{port} - {e}")
    return {"ip": ip, "port": port, "status": "Closed"}

def run(targets: list, config: dict) -> list:
    """Run a multi-threaded port scan on a list of targets"""
    results = []
    runner = ParallelRunner(config)

    for target in targets:
        ip = target["ip"]
        ports = range(1, int(config["scan"]["port_range"].split("-")[1]) + 1)

        LOGGER.info(f"Scanning ports on {ip}...")
        with ThreadPoolExecutor(max_workers=runner.max_threads) as executor:
            futures = [executor.submit(scan_port, ip, port) for port in ports]
            for future in futures:
                res = future.result()
                if res["status"] == "Open":
                    results.append(res)
    return results
  
