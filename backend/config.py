# backend/config.py
import json
import os

CONFIG_FILE = "config/default_config.json"
DEFAULT_CONFIG = {"tax_rate_percent": 18.0, "currency_symbol": "₹"}

def ensure_config_dir():
    d = os.path.dirname(CONFIG_FILE)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def load_config():
    ensure_config_dir()
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(cfg):
    ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

CONFIG = load_config()
