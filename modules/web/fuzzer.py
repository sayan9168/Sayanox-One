import requests
from concurrent.futures import ThreadPoolExecutor
from utils.logger import LOGGER

def run(base_url: str, config: dict) -> list:
    """Directory/file brute‑force"""
    found = []
    wordlist = open("config/wordlists/directories.txt").read().splitlines()
    with ThreadPoolExecutor(max_workers=config["general"]["max_threads"]) as ex:
        def check(path):
            try:
                u = f"{base_url.rstrip('/')}/{path}"
                r = requests.head(u, timeout=5, allow_redirects=False)
                if 200 <= r.status_code < 400:
                    found.append({"path": u, "status": r.status_code})
            except Exception:
                pass
        list(ex.map(check, wordlist))
    return found
  
