import ipaddress
import socket
from urllib.parse import urlparse
from utils.logger import LOGGER

def resolve_hostname(host: str):
    try:
        return socket.gethostbyname_ex(host)[2]
    except Exception:
        return []

def validate_target(target: str, config: dict):
    """Strict real‑world validation — prevents scanning invalid/protected ranges"""
    if not target:
        return False

    # Format check
    valid_types = [False, False, False]
    try:
        ipaddress.ip_address(target)
        valid_types[0] = True
    except ValueError:
        try:
            ipaddress.ip_network(target, strict=False)
            valid_types[1] = True
        except ValueError:
            try:
                res = urlparse(f"http://{target}")
                valid_types[2] = bool(res.netloc)
            except Exception:
                pass

    if not any(valid_types):
        LOGGER.error(f"Invalid target format: {target}")
        return False

    # Allowlist check — critical for real use
    if config["general"].get("enforce_allowlist", True):
        with open(config["general"]["allowlist_file"]) as f:
            allowed = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        if not any(allowed_target in target for allowed_target in allowed):
            LOGGER.error(f"⚠️ Target {target} NOT in allowlist — blocked")
            return False

    # Block private loopback unless explicitly allowed
    if any(net in target for net in ("127.0.0.", "::1", "192.168.", "10.")) and not config["general"].get("allow_local", False):
        LOGGER.warning("Local/private scanning disabled by default")
    return True
    
