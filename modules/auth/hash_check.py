import hashlib
from utils.logger import LOGGER

def guess_hash(hash_str: str, wordlist_path: str) -> str:
    """Simple MD5/SHA1 cracker"""
    with open(wordlist_path) as f:
        for word in f:
            w = word.strip()
            if hashlib.md5(w.encode()).hexdigest() == hash_str:
                return w
            if hashlib.sha1(w.encode()).hexdigest() == hash_str:
                return w
    return ""
  
