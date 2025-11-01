def low_stock_report(self):
    c = self.conn.cursor()
    c.execute("SELECT sku,name,qty,reorder_level FROM items WHERE qty <= reorder_level ORDER BY qty")
    rows = c.fetchall()
    if not rows:
        messagebox.showinfo("Low stock report", "No low-stock items")
        return
    txt = "Low stock items:\n\n"
    for r in rows:
        txt += f"{r[1]} [{r[0]}] - Qty {r[2]} (Reorder at {r[3]})\n"
    ReportDialog(self.root, "Low Stock Report", txt)

def sales_report_dialog(self):
    dlg = DateRangeDialog(self.root, title="Sales Report")
    if dlg.result:
        start, end = dlg.result
        # include end day full day
        start_iso = start.isoformat()
        end_iso = (end + timedelta(days=1)).isoformat()
        c = self.conn.cursor()
        c.execute("SELECT id,created_at,total,user FROM invoices WHERE created_at >= ? AND created_at < ? ORDER BY created_at",
                  (start_iso, end_iso))
        invs = c.fetchall()
        if not invs:
            messagebox.showinfo("Sales", "No invoices in range")
            return
        rows_txt = "Invoices:\n\n"
        rows_csv = [["id","created_at","total","user"]]
        for inv in invs:
            rows_txt += f"#{inv[0]} {inv[1]}  {CONFIG.get('currency_symbol')} {inv[2]:.2f} by {inv[3]}\n"
            rows_csv.append([inv[0],inv[1],f"{inv[2]:.2f}",inv[3]])
        dlg2 = ReportDialog(self.root, "Sales Report", rows_txt, csv_rows=rows_csv)
