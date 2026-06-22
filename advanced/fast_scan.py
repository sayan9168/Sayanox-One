from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from utils.logger import LOGGER

class ParallelRunner:
    def __init__(self, config):
        self.max_threads = min(config["general"]["max_threads"], 100)
        self.timeout = config["general"]["timeout"] / 1000
        self.delay = config["scan"]["evasion"].get("delay_ms", 0) / 1000

    def run(self, func, items, fail_fast=False):
        """Run tasks safely, never hang, return results even if some fail"""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_threads) as ex:
            futures = {ex.submit(func, item): item for item in items}
            for f in as_completed(futures, timeout=self.timeout * len(items)):
                try:
                    results.append(f.result(timeout=self.timeout))
                    if self.delay > 0:
                        time.sleep(self.delay)
                except Exception as e:
                    LOGGER.debug(f"Task failed: {type(e).__name__}")
                    if fail_fast:
                        raise
        return results
        
