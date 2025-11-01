def open_invoice_html(self, invoice_id):
    c = self.conn.cursor()
    c.execute("SELECT id,created_at,total,tax,discount,user FROM invoices WHERE id=?", (invoice_id,))
    inv = c.fetchone()
    if not inv:
        messagebox.showerror("Error","Invoice not found")
        return
    lines = []
    c.execute("SELECT sku,name,unit_price,quantity,discount,line_total FROM invoice_lines WHERE invoice_id=?", (invoice_id,))
    for r in c.fetchall():
        lines.append(r)
    rows_html=""
    subtotal = 0.0
    for r in lines:
        sku,name,unit,qty,ldisc,ltotal = r
        rows_html += f"<tr><td>{sku}</td><td>{name}</td><td align='right'>{unit:.2f}</td><td align='center'>{qty}</td><td align='right'>{ldisc:.2f}%</td><td align='right'>{ltotal:.2f}</td></tr>"
        subtotal += ltotal
    created_at = inv[1]
    total = inv[2]
    tax = inv[3] or 0.0
    discount = inv[4] or 0.0
    user = inv[5] or "unknown"
    html = f"""
    <html><head><meta charset="utf-8"><title>Invoice #{invoice_id}</title></head>
    <body>
    <h2>{APP_NAME} - Invoice #{invoice_id}</h2>
    <p>Date: {created_at}</p>
    <p>Cashier: {user}</p>
    <table border="1" cellpadding="6" cellspacing="0">
    <tr><th>SKU</th><th>Name</th><th>Unit</th><th>Qty</th><th>LineDisc%</th><th>LineTotal</th></tr>
    {rows_html}
    </table>
    <p>Subtotal: {CONFIG.get('currency_symbol')} {subtotal:.2f}</p>
    <p>Discount: {CONFIG.get('currency_symbol')} {discount:.2f}</p>
    <p>Tax: {CONFIG.get('currency_symbol')} {tax:.2f}</p>
    <h3>Total: {CONFIG.get('currency_symbol')} {total:.2f}</h3>
    </body></html>
    """
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8")
    tmp.write(html)
    tmp.close()
    webbrowser.open(f"file://{tmp.name}")
