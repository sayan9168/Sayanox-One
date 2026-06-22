import time
import random
import socket
from utils.logger import LOGGER

class StealthEngine:
    def __init__(self, config):
        self.cfg = config["scan"]["evasion"]
        self.ua_pool = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130",
            "Mozilla/5.0 (X11; Linux x86_64) Firefox/128",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605"
        ]

    def delay(self):
        """Adaptive delay so we don't look like a bot"""
        if self.cfg.get("enabled", False):
            base = self.cfg.get("delay_ms", 150) / 1000
            time.sleep(base + random.uniform(0, base*1.5))

    def patch_headers(self, headers: dict):
        headers["User-Agent"] = random.choice(self.ua_pool)
        headers["Accept-Language"] = "en-US,en;q=0.9"
        headers["X-Forwarded-For"] = f"{random.randint(1,254)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        return headers

    def fragment_packet(self, sock: socket.socket):
        """Lower‑level evasion if supported"""
        if self.cfg.get("fragment_packets", False):
            try:
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_MTU_DISCOVER, 0)
            except Exception:
                pass
                
