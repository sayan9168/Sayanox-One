import ipaddress
from urllib.parse import urlparse
from utils.logger import LOGGER

def is_ip(target: str) -> bool:
    """Check if the target is a valid IP address"""
    try:
        ipaddress.ip_address(target)
        return True
    except ipaddress.AddressValueError:
        return False

def is_domain(target: str) -> bool:
    """Check if the target is a valid domain"""
    try:
        result = urlparse(f"http://{target}")
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_cidr(target: str) -> bool:
    """Check if the target is a valid CIDR range"""
    try:
        ipaddress.ip_network(target, strict=False)
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False

def validate_target(target: str, config: dict) -> bool:
    """Full validation of the target against allowlists and type checks"""
    # Check target type
    if not any([is_ip(target), is_domain(target), is_cidr(target)]):
        LOGGER.error(f"Invalid target format: {target}")
        return False

    # Check against allowlist (if enabled)
    if config.get("general", {}).get("use_allowlist", False):
        with open(config["general"]["allowlist_file"], "r") as f:
            allowed = [line.strip() for line in f if line.strip()]
        if target not in allowed:
            LOGGER.error(f"Target {target} is not in the allowlist.")
            return False

    return True
          
