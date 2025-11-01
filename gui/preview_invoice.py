def preview_invoice(self):
    # create temp preview html from current cart (not saved)
    if not self.cart:
        messagebox.showinfo("Info","Cart empty")
        return
    html = self.generate_invoice_html_preview()
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8")
    tmp.write(html)
    tmp.close()
    webbrowser.open(f"file://{tmp.name}")

def generate_invoice_html_preview(self):
    subtotal = sum(it['ltotal'] for it in self.cart)
    ovd = float(self.overall_discount_entry.get().strip() or 0)
    if self.discount_mode_var.get()=="percent":
        discount = subtotal * (ovd/100.0)
    else:
        discount = ovd
    subtotal_after = max(0.0, subtotal - discount)
    tax_percent = float(self.tax_var.get().strip() or CONFIG.get("tax_rate_percent",18.0))
    tax = subtotal_after * (tax_percent/100.0)
    total = round(subtotal_after + tax,2)
    rows_html = ""
    for it in self.cart:
        rows_html += f"<tr><td>{it['sku']}</td><td>{it['name']}</td><td align='right'>{it['unit']:.2f}</td><td align='center'>{it['qty']}</td><td align='right'>{it['ldisc']:.2f}%</td><td align='right'>{it['ltotal']:.2f}</td></tr>"
    html = f"""
    <html><head><meta charset="utf-8"><title>Invoice Preview</title></head>
    <body>
    <h2>{APP_NAME} - Invoice Preview</h2>
    <p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <table border="1" cellpadding="6" cellspacing="0">
    <tr><th>SKU</th><th>Name</th><th>Unit</th><th>Qty</th><th>LineDisc%</th><th>LineTotal</th></tr>
    {rows_html}
    </table>
    <p>Subtotal: {CONFIG.get('currency_symbol')} {subtotal:.2f}</p>
    <p>Discount: {CONFIG.get('currency_symbol')} {discount:.2f}</p>
    <p>Tax ({tax_percent}%): {CONFIG.get('currency_symbol')} {tax:.2f}</p>
    <h3>Total: {CONFIG.get('currency_symbol')} {total:.2f}</h3>
    </body></html>
    """
    return html
