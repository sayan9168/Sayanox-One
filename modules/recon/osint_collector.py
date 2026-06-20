import requests
from utils.logger import LOGGER

def run(target: str, config: dict) -> dict:
    """Collect public OSINT data from common sources"""
    info = {"emails": [], "links": [], "hosts": []}
    try:
        # Example: Certificate Transparency log check
        r = requests.get(f"https://crt.sh/?q=%25.{target}&output=json", timeout=15)
        if r.status_code == 200:
            seen = set()
            for entry in r.json():
                name = entry["name_value"].lower()
                if name not in seen:
                    seen.add(name)
                    info["hosts"].append(name)
    except Exception as e:
        LOGGER.debug(f"OSINT source error: {e}")
    return info
  
