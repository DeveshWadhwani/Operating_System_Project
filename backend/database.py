import sqlite3, os, json, hashlib
from .logger import log_info, log_err

DB_FILE = "data/inventory_win.db"
CONFIG_FILE = "config/default_config.json"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()
def parse_money(s):
    s = str(s).strip()
    if not s:
        return 0.0
    try:
        return float(s)
    except Exception:
        raise ValueError("Invalid money value")    

def load_config():
    default_cfg = {"tax_rate_percent": 18.0, "currency_symbol": "₹"}
    ensure_dir(os.path.dirname(CONFIG_FILE))
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_cfg, f, indent=2)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

CONFIG = load_config()

def init_db():
    ensure_dir(os.path.dirname(DB_FILE))
    new = not os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT UNIQUE,
        name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL,
        qty INTEGER NOT NULL,
        reorder_level INTEGER DEFAULT 0
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        total REAL NOT NULL,
        tax REAL,
        discount REAL,
        user TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS invoice_lines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER,
        item_id INTEGER,
        sku TEXT,
        name TEXT,
        unit_price REAL,
        quantity INTEGER,
        discount REAL,
        line_total REAL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        role TEXT
    )''')

    conn.commit()
    if new:
        log_info("New database created.")
    return conn
