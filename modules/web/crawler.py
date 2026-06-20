import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from advanced.stealth_bypass import StealthEngine
from utils.logger import LOGGER

def run(url: str, config: dict) -> list:
    """Simple web crawler to find all reachable paths"""
    found = set()
    queue = [url]
    stealth = StealthEngine(config)
    max_depth = config["scan"].get("max_depth", 3)

    while queue and max_depth > 0:
        page = queue.pop(0)
        if page in found:
            continue
        found.add(page)
        try:
            resp = requests.get(page, headers=stealth.patch_headers({}), timeout=10)
            stealth.delay()
            soup = BeautifulSoup(resp.text, "html.parser")
            for a in soup.find_all("a", href=True):
                new_url = urljoin(url, a["href"].split("#")[0])
                if new_url.startswith(url) and new_url not in found:
                    queue.append(new_url)
        except Exception as e:
            LOGGER.debug(f"Crawl fail: {e}")
        max_depth -= 1
    return sorted(found)
  
