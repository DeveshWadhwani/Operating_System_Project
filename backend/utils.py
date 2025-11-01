# backend/utils.py
import hashlib
import os

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def parse_money(s):
    s = str(s).strip()
    if not s:
        return 0.0
    try:
        return float(s)
    except Exception:
        raise ValueError("Invalid money value")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
