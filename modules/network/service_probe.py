import socket
from utils.logger import LOGGER

def run(ip: str, ports: list) -> list:
    """Grab simple service banners"""
    info = []
    for p in ports:
        try:
            s = socket.create_connection((ip, p), timeout=3)
            s.send(b"HEAD / HTTP/1.1\r\nHost: %s\r\n\r\n" % ip.encode())
            banner = s.recv(2048).decode(errors="ignore")
            info.append({"port": p, "banner": banner[:100]})
        except Exception:
            continue
    return info
  
