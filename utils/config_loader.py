import yaml
from utils.logger import LOGGER

def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        LOGGER.error(f"Config load failed: {e}")
        raise
      
