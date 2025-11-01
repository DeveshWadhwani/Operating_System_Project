import logging, os

LOG_FILE = "data/inventory_win.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

def log_info(msg):
    logging.info(msg)

def log_err(msg):
    logging.exception(msg)
