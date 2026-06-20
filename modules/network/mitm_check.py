import ssl
import socket
from utils.logger import LOGGER

def run(host: str, port: int = 443) -> dict:
    """Check certificate validity & basic TLS config"""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.create_connection((host, port), 5), server_hostname=host) as s:
            cert = s.getpeercert()
            return {"valid": bool(cert), "subject": dict(x[0] for x in cert["subject"])}
    except Exception as e:
        LOGGER.debug(f"TLS check: {e}")
        return {"valid": False, "error": str(e)}
      
