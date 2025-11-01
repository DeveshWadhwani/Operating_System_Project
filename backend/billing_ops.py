import csv, sqlite3
from datetime import datetime
from tkinter import filedialog, messagebox
from .logger import log_info, log_err

def import_inventory_csv(conn):
    fn = filedialog.askopenfilename(filetypes=[("CSV files","*.csv"),("All files","*.*")])
    if not fn:
        return
    try:
        with open(fn, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            c = conn.cursor()
            count = 0
            for row in reader:
                sku = row.get("sku") or ""
                name = row.get("name") or ""
                if not name:
                    continue
                price = float(row.get("price") or 0)
                qty = int(float(row.get("qty") or 0))
                reorder = int(float(row.get("reorder_level") or 0))
                cat = row.get("category") or ""
                try:
                    c.execute("INSERT INTO items (sku,name,category,price,qty,reorder_level) VALUES (?,?,?,?,?,?)",
                              (sku, name, cat, price, qty, reorder))
                    count += 1
                except sqlite3.IntegrityError:
                    c.execute("UPDATE items SET category=?,price=?,qty=?,reorder_level=? WHERE sku=?",
                              (cat, price, qty, reorder, sku))
                    count += 1
            conn.commit()
            messagebox.showinfo("Import Successful", f"Imported {count} items.")
            log_info(f"Imported inventory CSV: {fn}")
    except Exception as e:
        log_err(str(e))
        messagebox.showerror("Error", str(e))
