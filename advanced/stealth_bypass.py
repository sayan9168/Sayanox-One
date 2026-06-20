import time
import random
from utils.logger import LOGGER

class StealthEngine:
    def __init__(self, config):
        self.cfg = config["scan"]["evasion"]

    def delay(self):
        """Randomized delay to avoid rate‑limits"""
        if self.cfg["enabled"]:
            t = self.cfg["delay_ms"] / 1000.0
            time.sleep(t + random.uniform(0, t*0.5))

    def patch_headers(self, headers: dict):
        """Randomize headers to look like different clients"""
        headers["User‑Agent"] = random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (X11; Linux x86_64)"
        ])
        return headers
      
