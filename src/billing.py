import sqlite3
from datetime import datetime
import os
import tempfile

DB_PATH = os.path.join("data", "inventory.db")


def generate_bill(customer_name, items):
   
    total = sum(item['price'] * item['quantity'] for item in items)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO bills (customer_name, date, total) VALUES (?, ?, ?)",
              (customer_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total))
    conn.commit()
    conn.close()

    return total


def print_bill(bill_text):
    """
    Print the generated bill using the system's default printer.
    """
    temp_file = tempfile.mktemp(".txt")
    with open(temp_file, "w") as f:
        f.write(bill_text)
    os.startfile(temp_file, "print")


def clear_bill(entries):
    """
    Clear all billing input fields in the GUI.
    'entries' should be a list of Entry widgets.
    """
    for e in entries:
        e.delete(0, "end")
