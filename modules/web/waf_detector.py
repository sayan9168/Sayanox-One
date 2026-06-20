import requests
from utils.logger import LOGGER

def run(url: str, config: dict) -> dict:
    """Basic WAF detection via response headers/code"""
    try:
        r = requests.get(url, timeout=10)
        sigs = ["cloudflare", "akamai", "imperva", "mod_security", "sucuri"]
        detected = []
        for h,v in r.headers.items():
            for s in sigs:
                if s in h.lower() or s in v.lower():
                    detected.append(s)
        return {"waf_detected": bool(detected), "names": list(set(detected))}
    except Exception as e:
        LOGGER.debug(f"WAF detect: {e}")
        return {"waf_detected": False, "names": []}
      
