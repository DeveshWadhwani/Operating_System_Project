import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join("data", "inventory.db")


def init_db():
    """
    Initialize the database and create required tables.
    """
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS bills (
                    bill_no INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT,
                    date TEXT,
                    total REAL
                )''')

    conn.commit()
    conn.close()


def add_product(name, price, quantity):
    """
    Add a new product to the inventory database.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
              (name, price, quantity))
    conn.commit()
    conn.close()


def update_product(pid, name, price, quantity):
    """
    Update existing product details.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE products SET name=?, price=?, quantity=? WHERE id=?",
              (name, price, quantity, pid))
    conn.commit()
    conn.close()


def delete_product(pid):
    """
    Delete a product from the inventory.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()


def search_product(pid):
    """
    Retrieve product details by ID.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id=?", (pid,))
    data = c.fetchone()
    conn.close()
    return data
