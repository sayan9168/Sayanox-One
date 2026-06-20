from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
from advanced.stealth_bypass import StealthEngine
from utils.logger import LOGGER

def run(url: str, config: dict) -> list:
    payloads = ["<script>alert(1)</script>", "\" onload=alert(1)>", "' onmouseover=alert(1)//"]
    results = []
    stealth = StealthEngine(config)
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)

    for param in params:
        for pay in payloads:
            test_params = params.copy()
            test_params[param] = pay
            new_q = urlencode(test_params, doseq=True)
            test_url = urlunparse(parsed._replace(query=new_q))
            try:
                r = requests.get(test_url, headers=stealth.patch_headers({}), timeout=8)
                stealth.delay()
                if pay in r.text:
                    results.append({
                        "type": "Reflected XSS",
                        "param": param,
                        "severity": "High",
                        "url": test_url
                    })
            except Exception as e:
                LOGGER.debug(f"XSS error: {e}")
    return results
  
