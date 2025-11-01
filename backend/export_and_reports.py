def export_cart_csv(self):
    if not self.cart:
        messagebox.showinfo("Info","Cart empty")
        return
    fn = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if not fn:
        return
    try:
        with open(fn, "w", newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(["sku","name","unit_price","qty","line_discount_percent","line_total"])
            for it in self.cart:
                w.writerow([it['sku'], it['name'], f"{it['unit']:.2f}", it['qty'], f"{it['ldisc']:.2f}", f"{it['ltotal']:.2f}"])
        messagebox.showinfo("Exported", f"Cart exported to {fn}")
        log_info(f"Exported cart CSV to {fn}")
    except Exception as e:
        log_err("Export cart failed")
        messagebox.showerror("Error", str(e))
