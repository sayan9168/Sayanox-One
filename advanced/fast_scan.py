from concurrent.futures import ThreadPoolExecutor
from utils.logger import LOGGER

class ParallelRunner:
    def __init__(self, config):
        self.max_threads = config["general"]["max_threads"]

    def run(self, func, items):
        with ThreadPoolExecutor(max_workers=self.max_threads) as ex:
            return list(ex.map(func, items))
          
